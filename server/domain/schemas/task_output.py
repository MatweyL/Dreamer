from uuid import UUID

from pydantic import BaseModel


class InputTaskOutput(BaseModel):
    pass


class TaskOutputPK(BaseModel):
    task_uid: UUID


class TaskInput(TaskOutputPK, InputTaskOutput):
    pass
