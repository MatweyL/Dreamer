from typing import Optional, Dict
from uuid import UUID

from pydantic import BaseModel

from server.domain.schemas import FieldTypes
from server.domain.schemas.task import TaskTypePK, TaskPK


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
    previous_task: Optional[TaskPK] = None
    current_task: Optional[TaskPK] = None


class PipelineInput(BaseModel):
    task_input_by_type: Dict[int, int]


class TaskDataTemplatePK(BaseModel):
    is_input: bool
    field_name: str
    task_type_uid: UUID


class TaskDataTemplate(TaskDataTemplatePK):
    field_type: FieldTypes
    is_list: bool
