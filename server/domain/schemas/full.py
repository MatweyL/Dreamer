from typing import List, Optional

from server.domain.schemas import Task, TaskType, TaskData, PipelineStep, PipelineExecution, TaskDataTemplate, \
    TaskStatusLog


class FullTask(Task):
    type: TaskType
    data_input: List[TaskData]
    data_output: Optional[List[TaskData]] = None
    data_output_template: List[TaskDataTemplate]


class FullPipelineStep(PipelineStep):
    pipeline_execution: PipelineExecution
    previous_task: Optional[FullTask] = None
    current_task: FullTask


class FullTaskStatus(TaskStatusLog):
    output: Optional[List[TaskData]] = None
