from abc import ABC

from server.domain.schemas.task import TaskStatusLog, TaskStatusLogPK, Task, TaskPK, TaskTypePK, TaskType
from server.ports.outbound.repository.abstract import AbstractRepository


class AbstractTaskTypeRepository(AbstractRepository[TaskType, TaskType, TaskTypePK], ABC):
    pass


class AbstractTaskRepository(AbstractRepository[Task, Task, TaskPK], ABC):
    pass


class AbstractTaskStatusLogRepository(AbstractRepository[TaskStatusLog, TaskStatusLog, TaskStatusLogPK], ABC):
    pass
