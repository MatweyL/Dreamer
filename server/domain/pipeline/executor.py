from typing import Optional

from pydantic import BaseModel

from server.common.logs import logger
from server.domain.interfaces import FullPipelineStepBuilderInterface
from server.domain.schemas import PipelineExecution, TaskStatus, PipelineStep
from server.ports.outbound.repository.domain.pipeline import AbstractPipelineStepRepository
from server.ports.outbound.repository.domain.task import AbstractTaskRepository
from server.ports.outbound.repository.queries import FilterFields, Field


class PipelineState(BaseModel):
    in_progress: bool
    is_finished: bool
    can_execute_step: bool
    step_to_execute: Optional[PipelineStep]


class PipelineExecutor:

    def __init__(self,
                 pipeline_step_repo: AbstractPipelineStepRepository,
                 task_repo: AbstractTaskRepository,
                 full_pipeline_step_builder: FullPipelineStepBuilderInterface,
                 pipeline_step_producer):
        self._pipeline_step_repo = pipeline_step_repo
        self._task_repo = task_repo
        self._full_pipeline_step_builder = full_pipeline_step_builder
        self._pipeline_step_producer = pipeline_step_producer

    async def get_pipeline_state(self, pipeline_execution: PipelineExecution) -> PipelineState:
        is_finished = False
        in_progress = False
        can_execute_step = False

        previous_task_uid = None
        while True:
            # 1. Получить следующий шаг пайплайна
            filter_fields = FilterFields(group=[Field(name='previous_task_uid', value=previous_task_uid),
                                                Field(name='pipeline_execution_uid', value=pipeline_execution.uid)])
            current_step = await self._pipeline_step_repo.filter_one(filter_fields)
            if not current_step:  # достигли конца пайплайна - он выполнен полностью
                is_finished = True
                logger.warning(f'pipeline already finished: {pipeline_execution}')
                break
            # 2. Получить подробную информацию о задаче
            current_task = await self._task_repo.get(current_step.current_task)
            if current_task.status in (TaskStatus.CREATED, TaskStatus.ERROR):
                logger.info(f'pipeline will continue with step: {current_task}')
                can_execute_step = True
                break
            elif current_task.status in (TaskStatus.QUEUED, TaskStatus.IN_WORK):  # Шаг уже исполняется, нельзя начинать исполнение шага
                in_progress = True
                logger.info(f'pipeline in progress: {current_task}; break against try of task execution')
                break
            previous_task_uid = current_task.uid  # 3. Переходим к следующему шагу пайплайна

        return PipelineState(in_progress=in_progress,
                             is_finished=is_finished,
                             can_execute_step=can_execute_step,
                             step_to_execute=current_step)

    async def run_pipeline_step(self, pipeline_execution: PipelineExecution):
        pipeline_state = await self.get_pipeline_state(pipeline_execution)
        logger.info(pipeline_state)
        if pipeline_state.can_execute_step:
            logger.info('produce pipeline step for execution')
            full_pipeline_step = await self._full_pipeline_step_builder.build(pipeline_state.step_to_execute)
            await self._pipeline_step_producer.produce(full_pipeline_step)

