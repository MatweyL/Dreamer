from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel

from server.domain.schemas import TaskStatus


class VideoToImagePipelineRq(BaseModel):
    internal_url: str
    text_size: int
    style: str
    negative_prompt: str
    num_inference_steps: int
    images_number: int


class VideoToImagePipelineRs(BaseModel):
    pipeline_execution_uid: UUID


class PipelineExecutionListRq(BaseModel):
    pass


class PipelineExecutionListRs(BaseModel):
    pipeline_execution: List[UUID]


class PipelineResultRq(BaseModel):
    pass


class PipelineResultRs(BaseModel):
    is_finished: bool
    current_task: Optional[str]
    current_task_status: TaskStatus
    duration: float
    images_urls: Optional[List[str]] = None
