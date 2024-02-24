from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from server.domain.schemas.task import Task, TaskTypePK


class PipelinePK(BaseModel):  # объект Primary Key не должен содержать вложенных объектов
    uid: UUID


class Pipeline(PipelinePK):
    name: str


class PipelineStepTemplatePK(BaseModel):
    pipeline: PipelinePK  # достаточно иметь только идентификатор связанного объекта
    previous_task_type: TaskTypePK
    current_task_type: TaskTypePK


class PipelineStepTemplate(PipelineStepTemplatePK):
    pass


class PipelineExecutionPK(BaseModel):
    uid: UUID


class PipelineExecution(PipelineExecutionPK):
    pipeline: PipelinePK


class PipelineStepPK(BaseModel):
    uid: UUID


class PipelineStep(PipelineStepPK):
    pipeline_execution: PipelineExecutionPK
    previous_task: Optional[Task] = None
    current_task: Optional[Task] = None
