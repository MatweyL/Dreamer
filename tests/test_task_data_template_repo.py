from uuid import UUID

import pytest

from server.domain.schemas import PipelinePK
from server.ports.outbound.repository.queries import FilterFields, Field


@pytest.mark.asyncio
async def test_task_data_template_repo_crud(task_data_template_repo, task_type_repo):
    task_types = await task_type_repo.filter(FilterFields())
    assert task_types
    assert len(task_types) == 3
    for task_type in task_types:
        filter_field = Field(name='task_type_uid',
                             value=task_type.uid)
        task_data_template = await task_data_template_repo.filter(FilterFields(group=[filter_field]))
        assert task_data_template
