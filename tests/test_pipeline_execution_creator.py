
from uuid import UUID

import pytest

from server.domain.schemas import PipelinePK
from server.ports.outbound.repository.queries import FilterFields, Field


@pytest.mark.asyncio
async def test_pipeline_execution_creator(pipeline_execution_creator, pipeline, pipeline_input):
    pipeline_execution = await pipeline_execution_creator.create(pipeline, pipeline_input)
    assert pipeline_execution
