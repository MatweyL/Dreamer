from uuid import UUID

import pytest

from server.domain.schemas import PipelinePK
from server.ports.outbound.repository.queries import FilterFields, Field


@pytest.mark.asyncio
async def test_pipeline_repo_crud(pipeline_step_template_repo, pipeline_repo):
    filter_field = Field(name='pipeline_uid',
                         value='88884444-5157-45e3-a6c0-0901d6c292a0')
    pipeline_step_templates = await pipeline_step_template_repo.filter(FilterFields(group=[filter_field]))
    assert pipeline_step_templates

    assert len(pipeline_step_templates) == 3
    