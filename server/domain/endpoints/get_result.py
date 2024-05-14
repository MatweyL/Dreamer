from random import randint

from server.domain.endpoints.base import Endpoint
from server.domain.schemas import TaskStatus
from server.domain.schemas.endpoints import PipelineResultRq, PipelineResultRs


class GetPipelineResultEndpoint(Endpoint):

    async def execute(self, request: PipelineResultRq) -> PipelineResultRs:
        return PipelineResultRs(
            is_finished=False,
            current_task='test',
            current_task_status=TaskStatus.FINISHED,
            duration=randint(600, 900) * 1.0,
        )
