from server.domain.interfaces import FullPipelineStepBuilderInterface, FullTaskBuilderInterface
from server.domain.schemas import PipelineStepPK
from server.domain.schemas.full import FullPipelineStep
from server.ports.outbound.repository.domain.pipeline import AbstractPipelineStepRepository, AbstractPipelineRepository, \
    AbstractPipelineExecutionRepository


class FullPipelineStepBuilder(FullPipelineStepBuilderInterface):

    def __init__(self, pipeline_step_repo: AbstractPipelineStepRepository,
                 pipeline_execution_repo: AbstractPipelineExecutionRepository,
                 full_task_builder: FullTaskBuilderInterface):
        self._pipeline_step_repo = pipeline_step_repo
        self._pipeline_execution_repo = pipeline_execution_repo
        self._full_task_builder = full_task_builder

    async def build(self, pipeline_step_pk: PipelineStepPK) -> FullPipelineStep:
        pipeline_step = await self._pipeline_step_repo.get(pipeline_step_pk)
        pipeline_execution = await self._pipeline_execution_repo.get(pipeline_step.pipeline_execution)
        previous_task = None
        if pipeline_step.previous_task:
            previous_task = await self._full_task_builder.build(pipeline_step.previous_task)
        current_task = await self._full_task_builder.build(pipeline_step.current_task)
        full_pipeline_step = FullPipelineStep(uid=pipeline_step.uid,
                                              pipeline_execution=pipeline_execution,
                                              previous_task=previous_task,
                                              current_task=current_task)
        return full_pipeline_step
