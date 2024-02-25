from typing import Optional, Dict, Type
from uuid import UUID

from pydantic import BaseModel

from server.domain.schemas.task import TaskTypes
from server.domain.schemas.task import TaskTypePK, TaskPK
from server.domain.schemas.task_input import InputTaskInput, InputVideoToTextInput, InputTextToImageInput


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
    task_input_by_type: Dict[TaskTypes, InputTaskInput]


if __name__ == "__main__":
    pi = PipelineInput(task_input_by_type={
        TaskTypes.EXTRACT_VIDEO_DESCRIPTION: InputVideoToTextInput(),
        TaskTypes.GENERATE_IMAGE_FROM_TEXT: InputTextToImageInput()
    })
    print(pi)
