from uuid import UUID

from pydantic import BaseModel


class TaskOutputPK(BaseModel):
    task_uid: UUID


class TaskOutput(TaskOutputPK):
    pass


class DownloadVideoOutput(TaskOutputPK):
    service_url: str


class VideoToTextOutput(TaskOutputPK):
    text: str


class GeneratedImagePK(BaseModel):
    uid: UUID


class GeneratedImage(GeneratedImagePK):
    group_uid: UUID
    service_url: str


class TextToImageOutput(TaskOutputPK):
    group_uid: UUID
