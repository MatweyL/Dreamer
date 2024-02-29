from uuid import uuid4

from server.domain.interfaces import TaskDataServiceInterface
from server.domain.schemas import TaskData, TaskDataBody, TaskPK
from server.ports.outbound.repository.domain.task import AbstractTaskDataRepository


class TaskDataService(TaskDataServiceInterface):

    def __init__(self, task_data_repo: AbstractTaskDataRepository):
        self._task_data_repo = task_data_repo

    async def create(self, task: TaskPK, body: TaskDataBody, is_input: bool) -> TaskData:
        task_data = TaskData(uid=uuid4(), task=task, field_name=body.field_name,
                             field_type=body.field_type,
                             field_value_int=body.field_value_int,
                             field_value_float=body.field_value_float,
                             field_value_str=body.field_value_str,
                             field_value_datetime=body.field_value_datetime,
                             is_list=body.is_list, is_input=is_input)
        await self._task_data_repo.create(task_data)
        return task_data
