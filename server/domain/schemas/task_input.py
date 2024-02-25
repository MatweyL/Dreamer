from uuid import UUID

from pydantic import BaseModel


class InputTaskInput(BaseModel):
    pass


class TaskInputPK(BaseModel):
    task_uid: UUID


class InputVideoToTextInput(InputTaskInput):
    prompt: str = None
    style: str = None
    text_size: int = None


class InputTextToImageInput(InputTaskInput):
    images_number: int = 1
    tags: str = None
    style: str = None


class VideoToTextInput(TaskInputPK, InputVideoToTextInput):
    pass


class TextToImageInput(TaskInputPK, InputTextToImageInput):
    pass
