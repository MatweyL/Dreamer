from typing import Type
from uuid import uuid4

from pydantic import BaseModel

from server.domain.endpoints.base import Endpoint
from server.domain.schemas import PipelineInput
from server.domain.schemas.endpoints import VideoToImagePipelineRq, VideoToImagePipelineRs


class CreateExecutionEndpoint(Endpoint):
    async def execute(self, request: VideoToImagePipelineRq) -> VideoToImagePipelineRs:
        # PipelineInput
        return VideoToImagePipelineRs(pipeline_execution_uid=uuid4())
