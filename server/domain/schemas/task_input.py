from uuid import UUID

from pydantic import BaseModel


class InputTaskInput(BaseModel):
    pass


class TaskInputPK(BaseModel):
    task_uid: UUID


class TaskInput(TaskInputPK, InputTaskInput):
    pass
