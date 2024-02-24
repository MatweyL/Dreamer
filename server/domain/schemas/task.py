from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from server.domain.schemas.enums import TaskStatus


class TaskTypePK(BaseModel):
    uid: UUID


class TaskType(TaskTypePK):
    name: str


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

