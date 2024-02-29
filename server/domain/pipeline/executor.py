from server.domain.schemas import PipelineExecution
from server.ports.outbound.repository.domain.pipeline import AbstractPipelineStepRepository
from server.ports.outbound.repository.domain.task import AbstractTaskRepository
from server.ports.outbound.repository.queries import FilterFields, Field


class PipelineExecutor:

    def __init__(self, pipeline_step_repo: AbstractPipelineStepRepository,
                 task_repo: AbstractTaskRepository):
        self._pipeline_step_repo = pipeline_step_repo
        self._task_repo = task_repo

    async def receive_pipeline_execution(self, pipeline_execution: PipelineExecution):
        filter_fields = FilterFields(group=[Field(name='previous_task_uid', value=None),
                                            Field(name='pipeline_execution_uid', value=pipeline_execution.uid)])
        first_step = await self._pipeline_step_repo.filter_one(filter_fields)
        task = await self._task_repo.get(first_step.current_task)
