from datetime import datetime
from typing import Union
from uuid import uuid4

from server.domain.interfaces import TaskServiceInterface, TaskDataServiceInterface
from server.domain.schemas import TaskTypePK, Task, TaskStatus, TaskStatusLog, TaskPK
from server.domain.schemas.full import FullTaskStatus
from server.ports.outbound.repository.domain.task import AbstractTaskRepository, AbstractTaskStatusLogRepository
from server.ports.outbound.repository.queries import UpdateFields, Field


class TaskService(TaskServiceInterface):

    def __init__(self, task_repo: AbstractTaskRepository,
                 task_status_log_repo: AbstractTaskStatusLogRepository,
                 task_data_service: TaskDataServiceInterface):
        self._task_repo = task_repo
        self._task_status_log_repo = task_status_log_repo
        self._task_data_service = task_data_service

    async def create(self, task_type: TaskTypePK) -> Task:
        task = Task(uid=uuid4(), status=TaskStatus.CREATED, type=task_type)
        task_status_log = TaskStatusLog(task_uid=task.uid, created_timestamp=datetime.now(), status=task.status)
        await self._task_repo.create(task)
        await self._task_status_log_repo.create(task_status_log)
        return task

    async def update_status(self, task_status_log: Union[TaskStatusLog, FullTaskStatus]) -> Task:
        task_pk = TaskPK(uid=task_status_log.task_uid)
        task_updated = await self._task_repo.update(task_pk,
                                                    UpdateFields(group=[Field(name='status',
                                                                              value=task_status_log.status)]))
        await self._task_status_log_repo.create(task_status_log)
        if task_status_log.status == TaskStatus.FINISHED:
            for task_data in task_status_log.output:
                await self._task_data_service.create(task_data.task, task_data, task_data.is_input)
        return task_updated
