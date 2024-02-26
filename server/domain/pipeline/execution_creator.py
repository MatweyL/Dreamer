from typing import List, Dict
from uuid import uuid4

from server.domain.interfaces import TaskServiceInterface, TaskDataServiceInterface
from server.domain.schemas.pipeline import PipelinePK, PipelineStepTemplate, PipelineStep, PipelineExecution, \
    PipelineInput
from server.domain.schemas.task import TaskTypePK, Task
from server.ports.outbound.repository.domain.pipeline import AbstractPipelineStepTemplateRepository, \
    AbstractPipelineExecutionRepository, AbstractPipelineStepRepository
from server.ports.outbound.repository.queries import FilterFields, Field


class PipelineExecutionCreator:

    def __init__(self, pipeline_step_template_repo: AbstractPipelineStepTemplateRepository,
                 pipeline_execution_repo: AbstractPipelineExecutionRepository,
                 pipeline_step_repo: AbstractPipelineStepRepository,
                 task_service: TaskServiceInterface,
                 task_data_service: TaskDataServiceInterface):
        self._pipeline_step_template_repo = pipeline_step_template_repo
        self._pipeline_execution_repo = pipeline_execution_repo
        self._pipeline_step_repo = pipeline_step_repo
        self._task_service = task_service
        self._task_data_service = task_data_service

    async def create(self, pipeline_pk: PipelinePK, pipeline_input: PipelineInput) -> PipelineExecution:
        pipeline_execution = PipelineExecution(uid=uuid4(), pipeline=pipeline_pk)
        await self._pipeline_execution_repo.create(pipeline_execution)  # создали объект запуска паплайна

        pipeline_template: List[PipelineStepTemplate] = await self._pipeline_step_template_repo.filter(
            FilterFields(group=[Field(name='pipeline_uid', value=pipeline_pk.uid)]))

        task_by_type: Dict[TaskTypePK, Task] = {}
        for step in pipeline_template:
            task_type_pk = step.current_task_type
            task = await self._task_service.create(task_type_pk)  # создали задачу
            task_data_bodies = pipeline_input.get(task_type_pk.uid)  # получили входные данные задачи
            if task_data_bodies:
                for task_data_body in task_data_bodies:
                    await self._task_data_service.create(task, task_data_body, True)  # создали входные данные для задачи
            task_by_type[task_type_pk] = task

        for step_template in pipeline_template:
            pipeline_step = PipelineStep(
                uid=uuid4(),
                pipeline_execution=pipeline_execution,
                previous_task=task_by_type.get(step_template.previous_task_type),
                current_task=task_by_type.get(step_template.current_task_type),
            )
            await self._pipeline_step_repo.create(pipeline_step)
        return pipeline_execution
