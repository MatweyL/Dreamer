from uuid import UUID

import pytest

from server.adapters.outbound.repository.orm_sqlalchemy import models
from server.adapters.outbound.repository.orm_sqlalchemy.repositories import *
from server.adapters.outbound.repository.orm_sqlalchemy.settings import settings
from server.adapters.outbound.repository.orm_sqlalchemy.unit_of_work import UnitOfWork
from server.domain import schemas
from server.domain.pipeline.execution_creator import PipelineExecutionCreator
from server.domain.schemas import Pipeline, PipelineInput, TaskDataBody
from server.domain.task.data_service import TaskDataService
from server.domain.task.service import TaskService


@pytest.fixture(scope='session')
def db_url():
    return settings.get_db_url(async_mode=True)


@pytest.fixture(scope='session')
def unit_of_work(db_url):
    return UnitOfWork(db_url=db_url)


@pytest.fixture(scope='session')
def pipeline_repo(unit_of_work):
    return PipelineSQLAlchemyRepository(schemas.Pipeline, schemas.PipelinePK, models.Pipeline, unit_of_work)


@pytest.fixture(scope='session')
def pipeline_step_template_repo(unit_of_work):
    return PipelineStepTemplateSQLAlchemyRepository(schemas.PipelineStepTemplate, schemas.PipelineStepTemplatePK,
                                                    models.PipelineStepTemplate, unit_of_work)


@pytest.fixture(scope='session')
def task_data_template_repo(unit_of_work):
    return TaskDataTemplateSQLAlchemyRepository(schemas.TaskDataTemplate, schemas.TaskDataTemplatePK,
                                                models.TaskDataTemplate, unit_of_work)


@pytest.fixture(scope='session')
def task_type_repo(unit_of_work):
    return TaskTypeSQLAlchemyRepository(schemas.TaskType, schemas.TaskTypePK,
                                        models.TaskType, unit_of_work)


@pytest.fixture(scope='session')
def pipeline_execution_repo(unit_of_work):
    return PipelineExecutionSQLAlchemyRepository(schemas.PipelineExecution, schemas.PipelineExecutionPK,
                                                 models.PipelineExecution, unit_of_work)


@pytest.fixture(scope='session')
def pipeline_step_repo(unit_of_work):
    return PipelineStepSQLAlchemyRepository(schemas.PipelineStep, schemas.PipelineStepPK,
                                            models.PipelineStep, unit_of_work)


@pytest.fixture(scope='session')
def task_repo(unit_of_work):
    return TaskSQLAlchemyRepository(schemas.Task, schemas.TaskPK, models.Task, unit_of_work)


@pytest.fixture(scope='session')
def task_status_log_repo(unit_of_work):
    return TaskStatusLogSQLAlchemyRepository(schemas.TaskStatusLog, schemas.TaskStatusLogPK,
                                             models.TaskStatusLog, unit_of_work)


@pytest.fixture(scope='session')
def task_service(task_repo, task_status_log_repo, task_data_service):
    return TaskService(task_repo, task_status_log_repo, task_data_service)


@pytest.fixture(scope='session')
def task_data_repo(unit_of_work):
    return TaskDataSQLAlchemyRepository(schemas.TaskData, schemas.TaskDataPK,
                                        models.TaskData, unit_of_work)


@pytest.fixture(scope='session')
def task_data_service(task_data_repo):
    return TaskDataService(task_data_repo)


@pytest.fixture(scope='session')
def pipeline():
    return PipelinePK(uid=UUID('88884444-5157-45e3-a6c0-0901d6c292a0'))


@pytest.fixture(scope='session')
def pipeline_input():
    raw_mapping = {
        UUID('00008888-5157-45e3-a6c0-0901d6c292a0'): [{
            "field_name": "internal_url",
            "field_type": "STRING",
            "field_value_str": "https://mock.com/mp4.mp4",
            "is_list": False
        }],
        UUID('11118888-5157-45e3-a6c0-0901d6c292a0'): [{
            "field_name": "text_size",
            "field_type": "INTEGER",
            "field_value_int": 3200,
            "is_list": False
        }],
        UUID('22228888-5157-45e3-a6c0-0901d6c292a0'): [
            {
                "field_name": "style",
                "field_type": "STRING",
                "field_value_str": "cyberpunk",
                "is_list": False
            }]
    }
    return PipelineInput(
        task_data_body_by_type_uid={k: [TaskDataBody(**v) for v in lst] for k, lst in raw_mapping.items()}
    )


@pytest.fixture(scope='session')
def pipeline_execution_creator(pipeline_step_template_repo, pipeline_execution_repo, pipeline_step_repo,
                               task_service, task_data_service):
    return PipelineExecutionCreator(pipeline_step_template_repo,
                                    pipeline_execution_repo,
                                    pipeline_step_repo,
                                    task_service,
                                    task_data_service)
