from typing import Union

from server.domain.interfaces import TaskServiceInterface, PipelineExecutorI
from server.domain.schemas import TaskStatusLog, PipelineStep
from server.domain.schemas.full import FullTaskStatus
from server.ports.outbound.repository.domain.pipeline import AbstractPipelineStepRepository


class TaskRouter:

    def __init__(self, task_service: TaskServiceInterface,
                 pipeline_executor: PipelineExecutorI,
                 pipeline_step_repo: AbstractPipelineStepRepository):
        self._task_service = task_service
        self._pipeline_executor = pipeline_executor
        self._pipeline_step_repo = pipeline_step_repo

    async def receive_task_status_log(self, task_status_log: Union[TaskStatusLog, FullTaskStatus]):
        task = await self._task_service.update_status(task_status_log)
        step: PipelineStep = await self._pipeline_step_repo.filter_one({'task_uid': task_status_log.task_uid})
        pipeline_execution = step.pipeline_execution
        await self._pipeline_executor.run_pipeline_step(pipeline_execution)