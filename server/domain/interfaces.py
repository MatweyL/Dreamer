from abc import ABC, abstractmethod

from server.domain.schemas import PipelineStepPK
from server.domain.schemas.full import FullTask, FullPipelineStep
from server.domain.schemas.task import TaskTypePK, Task, TaskDataBody, TaskData, TaskPK


class PipelineService(ABC):
    pass


class PipelineExecutionService(ABC):
    pass


class PipelineStepTemplateService(ABC):
    pass


class PipelineStepService(ABC):
    pass


class TaskTypeService(ABC):
    pass


class TaskServiceInterface(ABC):

    @abstractmethod
    async def create(self, task_type: TaskTypePK) -> Task:
        pass


class TaskStatusLogService(ABC):
    pass


class TaskDataServiceInterface(ABC):

    @abstractmethod
    async def create(self, task: TaskPK, body: TaskDataBody, is_input: bool) -> TaskData:
        pass


class FullTaskBuilderInterface(ABC):

    @abstractmethod
    async def build(self, task: TaskPK) -> FullTask:
        pass


class FullPipelineStepBuilderInterface(ABC):

    @abstractmethod
    async def build(self, pipeline_step: PipelineStepPK) -> FullPipelineStep:
        pass
