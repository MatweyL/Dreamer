from sqlalchemy import Column, String, UUID, ForeignKey, Enum, DateTime, Boolean, TEXT, Integer, Float

from server.adapters.outbound.repository.orm_sqlalchemy.base import Base, TablenameMixin, UUIDMixin, LoadTimestampMixin
from server.domain.schemas import TaskStatus, FieldTypes


class Pipeline(Base, TablenameMixin, UUIDMixin, LoadTimestampMixin):
    name = Column(String(128), nullable=False, unique=True)


class PipelineStepTemplate(Base, TablenameMixin, LoadTimestampMixin):
    pipeline_uid = Column(UUID(as_uuid=True), ForeignKey('pipeline.uid'), primary_key=True)
    previous_task_type_uid = Column(UUID(as_uuid=True), ForeignKey('task_type.uid'))
    current_task_type_uid = Column(UUID(as_uuid=True), ForeignKey('task_type.uid'), primary_key=True)


class PipelineExecution(Base, TablenameMixin, UUIDMixin, LoadTimestampMixin):
    pipeline_uid = Column(UUID(as_uuid=True), ForeignKey('pipeline.uid'), nullable=False)


class PipelineStep(Base, TablenameMixin, UUIDMixin, LoadTimestampMixin):
    pipeline_execution_uid = Column(UUID(as_uuid=True), ForeignKey('pipeline_execution.uid'), nullable=False)
    previous_task_uid = Column(UUID(as_uuid=True), ForeignKey('task.uid'))
    current_task_uid = Column(UUID(as_uuid=True), ForeignKey('task.uid'), nullable=False)


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


class TaskDataTemplate(Base, TablenameMixin, LoadTimestampMixin):
    task_type_uid = Column(UUID(as_uuid=True), ForeignKey('task_type.uid'), primary_key=True)
    field_name = Column(String(64), primary_key=True)
    is_input = Column(Boolean, primary_key=True)
    field_type = Column(Enum(FieldTypes), nullable=False)
    is_list = Column(Boolean, nullable=False)


class TaskData(Base, TablenameMixin, UUIDMixin, LoadTimestampMixin):
    task_uid = Column(UUID(as_uuid=True), ForeignKey('task.uid'))
    field_name = Column(String(64), nullable=False)
    field_type = Column(Enum(FieldTypes), nullable=False)
    field_value_str = Column(TEXT)
    field_value_int = Column(Integer)
    field_value_float = Column(Float)
    field_value_datetime = Column(DateTime)
    is_input = Column(Boolean, nullable=False)
    is_list = Column(Boolean, nullable=False)
