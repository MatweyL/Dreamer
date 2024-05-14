import asyncio

from server.adapters.common.converter import ChainedConverter, StrToPydanticConverter
from server.adapters.common.settings import RabbitMQConnectionSettings
from server.adapters.inbound.rabbit.consumer import RabbitMQConsumer
from server.adapters.inbound.rabbit.settings import RabbitMQConsumerSettings
from server.adapters.outbound.producer.conifg import rabbit_producer_config
from server.adapters.outbound.producer.rabbit import RabbitProducer, RMQPipelineStepProducer
from server.adapters.outbound.repository.orm_sqlalchemy import models
from server.adapters.outbound.repository.orm_sqlalchemy.repositories import PipelineStepSQLAlchemyRepository, \
    TaskSQLAlchemyRepository, TaskStatusLogSQLAlchemyRepository, TaskDataSQLAlchemyRepository, \
    PipelineExecutionSQLAlchemyRepository, TaskDataTemplateSQLAlchemyRepository, TaskTypeSQLAlchemyRepository
from server.adapters.outbound.repository.orm_sqlalchemy.settings import settings
from server.adapters.outbound.repository.orm_sqlalchemy.unit_of_work import UnitOfWork
from server.common.logs import logger
from server.common.utils import get_rabbit_dsn
from server.domain import schemas
from server.domain.builders.pipeline import FullPipelineStepBuilder
from server.domain.builders.task import TaskFullBuilder
from server.domain.pipeline.executor import PipelineExecutor
from server.domain.schemas import TaskStatusLog
from server.domain.schemas.full import FullTaskStatus
from server.domain.task.data_service import TaskDataService
from server.domain.task.router import TaskRouter
from server.domain.task.service import TaskService


async def main():
    unit_of_work = UnitOfWork(db_url=settings.get_db_url(async_mode=True))
    pipeline_step_repo = PipelineStepSQLAlchemyRepository(schemas.PipelineStep, schemas.PipelineStepPK,
                                                          models.PipelineStep, unit_of_work)
    task_repo = TaskSQLAlchemyRepository(schemas.Task, schemas.TaskPK, models.Task, unit_of_work)
    task_status_log_repo = TaskStatusLogSQLAlchemyRepository(schemas.TaskStatusLog, schemas.TaskStatusLogPK,
                                                             models.TaskStatusLog, unit_of_work)
    task_data_repo = TaskDataSQLAlchemyRepository(schemas.TaskData, schemas.TaskDataPK, models.TaskData, unit_of_work)
    pipeline_execution_repo = PipelineExecutionSQLAlchemyRepository(schemas.PipelineExecution,
                                                                    schemas.PipelineExecutionPK,
                                                                    models.PipelineExecution, unit_of_work)
    task_type_repo = TaskTypeSQLAlchemyRepository(schemas.TaskType,
                                                  schemas.TaskTypePK,
                                                  models.TaskType, unit_of_work)
    task_data_template_repo = TaskDataTemplateSQLAlchemyRepository(schemas.TaskDataTemplate,
                                                                   schemas.TaskDataTemplatePK,
                                                                   models.TaskDataTemplate, unit_of_work)
    rmq_connection_settings = RabbitMQConnectionSettings()
    rabbit_producer = RabbitProducer(rmq_connection_settings.protocol, rmq_connection_settings.user,
                                     rmq_connection_settings.password,
                                     rmq_connection_settings.host, rmq_connection_settings.port,
                                     rmq_connection_settings.virtual_host, rabbit_producer_config.exchange_name,
                                     rabbit_producer_config.exchange_type, rabbit_producer_config.reconnect_timeout_s,
                                     rabbit_producer_config.produce_max_retries)
    full_task_builder = TaskFullBuilder(task_repo, task_type_repo, task_data_repo, task_data_template_repo)
    full_pipeline_step_builder = FullPipelineStepBuilder(pipeline_step_repo, pipeline_execution_repo, full_task_builder)
    pipeline_step_producer = RMQPipelineStepProducer(rabbit_producer)
    pipeline_executor = PipelineExecutor(pipeline_step_repo, task_repo, full_pipeline_step_builder,
                                         pipeline_step_producer)
    task_data_service = TaskDataService(task_data_repo)
    task_service = TaskService(task_repo, task_status_log_repo, task_data_service)
    task_router = TaskRouter(task_service, pipeline_executor, pipeline_step_repo)
    rmq_consumer_settings = RabbitMQConsumerSettings()
    connection_url = get_rabbit_dsn(rmq_connection_settings.protocol, rmq_connection_settings.user,
                                    rmq_connection_settings.password, rmq_connection_settings.host,
                                    rmq_connection_settings.port, rmq_connection_settings.virtual_host)
    rabbit_consumer = RabbitMQConsumer(connection_url, rmq_consumer_settings.prefetch_count,
                                       rmq_consumer_settings.reconnect_timeout)
    boot_objects = [rabbit_consumer, rabbit_producer]
    for boot_object in boot_objects:
        await boot_object.start()
    str_to_task_status_log = StrToPydanticConverter(TaskStatusLog)
    str_to_full_task_status = StrToPydanticConverter(FullTaskStatus)
    chained_converter = ChainedConverter(str_to_full_task_status, ChainedConverter(str_to_task_status_log, None))
    await rabbit_consumer.consume_queue(rmq_consumer_settings.queue_name,
                                        task_router.receive_task_status_log,
                                        chained_converter)
    try:
        await asyncio.Future()
    except BaseException as e:
        logger.exception(e)
    for boot_object in boot_objects:
        await boot_object.stop()


if __name__ == "__main__":
    asyncio.run(main())
    # uvicorn.run(app, host='0.0.0.0', port=7430)
