from abc import ABC, abstractmethod
from typing import Union

from server.domain.schemas import PipelineStepPK, PipelineExecution, PipelineState
from server.domain.schemas.full import FullTask, FullPipelineStep, FullTaskStatus
from server.domain.schemas.task import TaskTypePK, Task, TaskDataBody, TaskData, TaskPK, TaskStatusLog


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

    @abstractmethod
    async def update_status(self, task_status_log: Union[TaskStatusLog, FullTaskStatus]) -> Task:
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


class PipelineExecutorI(ABC):

    async def get_pipeline_state(self, pipeline_execution: PipelineExecution) -> PipelineState:
        pass

    async def run_pipeline_step(self, pipeline_execution: PipelineExecution):
        pass
