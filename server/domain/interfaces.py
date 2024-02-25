from abc import ABC, abstractmethod

from server.domain.schemas.pipeline import PipelinePK
from server.domain.schemas.task import TaskTypePK, Task
from server.domain.schemas.task_input import InputTaskInput


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


class TaskInputServiceInterface(ABC):

    @abstractmethod
    async def create(self, task: Task, input_task_input):
        pass
