import pytest


@pytest.mark.asyncio
async def test_pipeline_execution_creator(pipeline_execution_creator, pipeline, pipeline_input):
    pipeline_execution = await pipeline_execution_creator.create(pipeline, pipeline_input)
    assert pipeline_execution
