from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from server.domain.schemas.enums import TaskStatus, TaskTypes


class TaskTypePK(BaseModel):
    uid: UUID

    def __eq__(self, other):
        return self.uid == other.uid

    def __hash__(self):
        return hash(self.uid)


class TaskType(TaskTypePK):
    name: TaskTypes


class TaskPK(BaseModel):
    uid: UUID


class Task(TaskPK):
    type: TaskTypePK
    status: TaskStatus


class TaskStatusLogPK(BaseModel):
    task_uid: UUID
    created_timestamp: datetime


class TaskStatusLog(TaskStatusLogPK):
    status: TaskStatus
    description: str

