from datetime import datetime
from uuid import uuid4

import pytest

from server.domain.schemas import Pipeline
from server.ports.outbound.repository.queries import UpdateFields, Field, FilterFields


@pytest.mark.asyncio
async def test_pipeline_repo_crud(pipeline_repo):
    pipeline = Pipeline(uid=uuid4(), name=f'test_{datetime.now()}')
    created_pipeline = await pipeline_repo.create(pipeline)
    assert created_pipeline.uid == pipeline.uid
    new_name = f'new_pipeline_name_{datetime.now()}'
    updated_pipeline = await pipeline_repo.update(pipeline, UpdateFields(group=[Field(name='name', value=new_name)]))
    assert updated_pipeline
    assert updated_pipeline.name == new_name
    gotten_pipeline = await pipeline_repo.get(pipeline)
    assert gotten_pipeline
    assert gotten_pipeline.uid == pipeline.uid
    assert gotten_pipeline.name == new_name

    deleted_pipeline = await pipeline_repo.delete(pipeline)
    assert deleted_pipeline
    assert deleted_pipeline.uid == pipeline.uid


@pytest.mark.asyncio
async def test_pipeline_repo_filtering(pipeline_repo):
    all_pipelines = await pipeline_repo.filter(FilterFields())
    assert all_pipelines
    pipeline_first = all_pipelines[0]
    pipelines_filtered = await pipeline_repo.filter(FilterFields(group=[Field(name='uid', value=pipeline_first.uid)]))
    assert pipelines_filtered
    assert len(pipelines_filtered) == 1
    assert pipelines_filtered[0].uid == pipeline_first.uid
