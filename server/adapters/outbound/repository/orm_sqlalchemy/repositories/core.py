from server.adapters.outbound.repository.orm_sqlalchemy import models
from server.adapters.outbound.repository.orm_sqlalchemy.abstract import AbstractSQLAlchemyRepository
from server.domain import schemas
from server.domain.schemas import PipelinePK, TaskTypePK, PipelineExecutionPK, TaskPK
from server.ports.outbound.repository.domain.pipeline import AbstractPipelineRepository, \
    AbstractPipelineStepTemplateRepository, AbstractPipelineExecutionRepository, AbstractPipelineStepRepository, \
    AbstractTaskDataTemplateRepository
from server.ports.outbound.repository.domain.task import AbstractTaskTypeRepository, AbstractTaskRepository, \
    AbstractTaskStatusLogRepository, AbstractTaskDataRepository


class PipelineSQLAlchemyRepository(AbstractPipelineRepository, AbstractSQLAlchemyRepository):
    def domain_model(self, obj: models.Pipeline) -> schemas.Pipeline:
        return schemas.Pipeline(
            uid=obj.uid,
            name=obj.name
        )

    def entity_model(self, obj: schemas.Pipeline) -> models.Pipeline:
        return models.Pipeline(
            uid=obj.uid, name=obj.name
        )


class PipelineStepTemplateSQLAlchemyRepository(AbstractPipelineStepTemplateRepository, AbstractSQLAlchemyRepository):
    def domain_model(self, obj: models.PipelineStepTemplate) -> schemas.PipelineStepTemplate:
        return schemas.PipelineStepTemplate(
            pipeline=PipelinePK(uid=obj.pipeline_uid),
            previous_task_type=TaskTypePK(uid=obj.previous_task_type_uid),
            current_task_type=TaskTypePK(uid=obj.current_task_type_uid),
        )

    def entity_model(self, obj: schemas.PipelineStepTemplate) -> models.PipelineStepTemplate:
        return models.PipelineStepTemplate(
            pipeline_uid=obj.pipeline.uid, previous_task_type_uid=obj.previous_task_type.uid,
            current_task_type_uid=obj.current_task_type.uid
        )


class PipelineExecutionSQLAlchemyRepository(AbstractPipelineExecutionRepository, AbstractSQLAlchemyRepository):
    def domain_model(self, obj: models.PipelineExecution) -> schemas.PipelineExecution:
        return schemas.PipelineExecution(uid=obj.uid,
                                         pipeline=PipelinePK(uid=obj.pipeline_uid))

    def entity_model(self, obj: schemas.PipelineExecution) -> models.PipelineExecution:
        return models.PipelineExecution(uid=obj.uid,
                                        pipeline_uid=obj.pipeline.uid)


class PipelineStepSQLAlchemyRepository(AbstractPipelineStepRepository, AbstractSQLAlchemyRepository):
    def domain_model(self, obj: models.PipelineStep) -> schemas.PipelineStep:
        return schemas.PipelineStep(uid=obj.uid,
                                    pipeline_execution=PipelineExecutionPK(uid=obj.pipeline_execution_uid),
                                    previous_task=TaskPK(uid=obj.previous_task_uid),
                                    current_task=TaskPK(uid=obj.current_task_uid))

    def entity_model(self, obj: schemas.PipelineStep) -> models.PipelineStep:
        return models.PipelineStep(uid=obj.uid,
                                   pipeline_execution_uid=obj.pipeline_execution.uid,
                                   previous_task_uid=obj.previous_task.uid,
                                   current_task_uid=obj.current_task.uid
                                   )


class TaskTypeSQLAlchemyRepository(AbstractTaskTypeRepository, AbstractSQLAlchemyRepository):
    def domain_model(self, obj: models.TaskType) -> schemas.TaskType:
        return schemas.TaskType(uid=obj.uid, name=obj.name)

    def entity_model(self, obj: schemas.TaskType) -> models.TaskType:
        return models.TaskType(uid=obj.uid, name=obj.name)


class TaskSQLAlchemyRepository(AbstractTaskRepository, AbstractSQLAlchemyRepository):
    def domain_model(self, obj: models.Task) -> schemas.Task:
        return schemas.Task(uid=obj.uid, type=TaskTypePK(uid=obj.type_uid), status=obj.status)

    def entity_model(self, obj: schemas.Task) -> models.Task:
        return models.Task(uid=obj.uid, type_uid=obj.type.uid, status=obj.status)


class TaskStatusLogSQLAlchemyRepository(AbstractTaskStatusLogRepository, AbstractSQLAlchemyRepository):
    def domain_model(self, obj: models.TaskStatusLog) -> schemas.TaskStatusLog:
        return schemas.TaskStatusLog(task_uid=obj.task_uid, created_timestamp=obj.created_timestamp,
                                     status=obj.status, description=obj.description)

    def entity_model(self, obj: schemas.TaskStatusLog) -> models.TaskStatusLog:
        return models.TaskStatusLog(task_uid=obj.task_uid, created_timestamp=obj.created_timestamp,
                                    description=obj.description)


class TaskDataTemplateSQLAlchemyRepository(AbstractTaskDataTemplateRepository, AbstractSQLAlchemyRepository):
    def domain_model(self, obj: models.TaskDataTemplate) -> schemas.TaskDataTemplate:
        return schemas.TaskDataTemplate(is_input=obj.is_input,
                                        field_name=obj.field_name,
                                        task_type_uid=obj.task_type_uid,
                                        field_type=obj.field_type,
                                        is_list=obj.is_list

                                        )

    def entity_model(self, obj: schemas.TaskDataTemplate) -> models.TaskDataTemplate:
        return models.TaskDataTemplate(is_input=obj.is_input,
                                       field_name=obj.field_name,
                                       task_type_uid=obj.task_type_uid,
                                       field_type=obj.field_type,
                                       is_list=obj.is_list
                                       )


class TaskDataSQLAlchemyRepository(AbstractTaskDataRepository, AbstractSQLAlchemyRepository):
    def domain_model(self, obj: models.TaskData) -> schemas.TaskData:
        return schemas.TaskData(is_input=obj.is_input,
                                field_name=obj.field_name,
                                task=TaskPK(uid=obj.task_uid),
                                field_type=obj.field_type,
                                is_list=obj.is_list,
                                field_value=obj.field_value
                                )

    def entity_model(self, obj: schemas.TaskData) -> models.TaskData:
        return models.TaskData(is_input=obj.is_input,
                               field_name=obj.field_name,
                               task_uid=obj.task.uid,
                               field_type=obj.field_type,
                               is_list=obj.is_list,
                               field_value=obj.field_value
                               )
