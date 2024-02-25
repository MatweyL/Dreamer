from sqlalchemy import Column, String, UUID, ForeignKey, Enum, DateTime

from server.adapters.outbound.repository.orm_sqlalchemy.base import Base, TablenameMixin, UUIDMixin, LoadTimestampMixin
from server.domain.schemas import TaskStatus


class Pipeline(Base, TablenameMixin, UUIDMixin, LoadTimestampMixin):
    name = Column(String(128), nullable=False, unique=True)


class PipelineStepTemplate(Base, TablenameMixin, LoadTimestampMixin):
    pipeline_uid = Column(UUID(as_uuid=True), ForeignKey('pipeline.uid'), nullable=False)
    previous_task_type_uid = Column(UUID(as_uuid=True), ForeignKey('task_type.uid'))
    current_task_type_uid = Column(UUID(as_uuid=True), ForeignKey('task_type.uid'))


class PipelineExecution(Base, TablenameMixin, UUIDMixin, LoadTimestampMixin):
    pipeline_uid = Column(UUID(as_uuid=True), ForeignKey('pipeline.uid'), nullable=False)


class PipelineStep(Base, TablenameMixin, UUIDMixin, LoadTimestampMixin):
    pipeline_execution_uid = Column(UUID(as_uuid=True), ForeignKey('pipeline_execution.uid'), nullable=False)
    previous_task_uid = Column(UUID(as_uuid=True), ForeignKey('pipeline_execution.uid'))
    current_task_uid = Column(UUID(as_uuid=True), ForeignKey('pipeline_execution.uid'), nullable=False)


class TaskType(Base, TablenameMixin, UUIDMixin, LoadTimestampMixin):
    name = Column(String(128), nullable=False, unique=True)


class Task(Base, TablenameMixin, UUIDMixin, LoadTimestampMixin):
    type_uid = Column(UUID(as_uuid=True), ForeignKey('task_type.uid'), nullable=False)
    status = Column(Enum(TaskStatus), nullable=False)


class TaskStatusLog(Base, TablenameMixin, LoadTimestampMixin):
    task_uid = Column(UUID(as_uuid=True), ForeignKey('task.uid'), primary_key=True)
    created_timestamp = Column(DateTime, primary_key=True)
    status = Column(Enum(TaskStatus), nullable=False)
    description = Column(String(256))
