from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from server.domain.schemas.enums import TaskStatus, FieldTypes


class TaskTypePK(BaseModel):
    uid: UUID

    def __eq__(self, other):
        return self.uid == other.uid

    def __hash__(self):
        return hash(self.uid)


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


class TaskDataPK(BaseModel):
    uid: UUID


class TaskData(TaskDataPK):
    task: TaskPK
    field_name: str
    field_type: FieldTypes
    field_value: str
    is_input: bool
    is_list: bool
