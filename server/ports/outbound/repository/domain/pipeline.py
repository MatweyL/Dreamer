from abc import ABC

from server.domain.schemas.pipeline import Pipeline, PipelineStepTemplate, PipelineExecution, PipelineStepTemplatePK, \
    PipelineStep, PipelinePK, PipelineExecutionPK, PipelineStepPK, TaskDataTemplate, TaskDataTemplatePK
from server.ports.outbound.repository.abstract import AbstractRepository


class AbstractPipelineRepository(AbstractRepository[Pipeline, Pipeline, PipelinePK], ABC):
    pass


class AbstractPipelineStepTemplateRepository(AbstractRepository[
                                         PipelineStepTemplate,
                                         PipelineStepTemplate,
                                         PipelineStepTemplatePK], ABC):
    pass


class AbstractPipelineExecutionRepository(AbstractRepository[PipelineExecution,
                                                             PipelineExecution,
                                                             PipelineExecutionPK], ABC):
    pass


class AbstractPipelineStepRepository(AbstractRepository[PipelineStep, PipelineStep, PipelineStepPK], ABC):
    pass


class AbstractTaskDataTemplateRepository(AbstractRepository[TaskDataTemplate, TaskDataTemplate, TaskDataTemplatePK],
                                         ABC):
    pass
