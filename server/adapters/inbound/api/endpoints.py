from uuid import UUID

from fastapi import FastAPI

from server.domain.endpoints.create_executrion import CreateExecutionEndpoint
from server.domain.endpoints.get_result import GetPipelineResultEndpoint
from server.domain.schemas.endpoints import VideoToImagePipelineRq, VideoToImagePipelineRs, PipelineResultRq, \
    PipelineResultRs

app = FastAPI()


@app.post('/pipeline/execution')
async def create_pipeline_execution(request: VideoToImagePipelineRq) -> VideoToImagePipelineRs:
    return await CreateExecutionEndpoint().execute(request)


@app.get('/pipeline/execution')
async def get_pipeline_result(pipeline_execution_uid: UUID) -> PipelineResultRs:
    request = PipelineResultRq(pipeline_execution_uid=pipeline_execution_uid)
    return await GetPipelineResultEndpoint().execute(request)
