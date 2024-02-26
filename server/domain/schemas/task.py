from datetime import datetime
from typing import Annotated, Any, Optional
from uuid import UUID

from pydantic import BaseModel, BeforeValidator

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
    description: Optional[str] = None


class TaskDataPK(BaseModel):
    uid: UUID


def from_str_field_type(value: str):
    return FieldTypes(value)


def from_any_to_str(value: Any):
    return str(value)


class TaskDataBody(BaseModel):
    field_name: str
    field_type: Annotated[FieldTypes, BeforeValidator(from_str_field_type)]
    field_value: Annotated[str, BeforeValidator(from_any_to_str)]
    is_list: bool


class TaskData(TaskDataPK, TaskDataBody):
    task: TaskPK
    is_input: bool
