from server.domain.interfaces import TaskInputServiceInterface
from server.domain.schemas import Task


class TaskInputService(TaskInputServiceInterface):

    async def create(self, task: Task, input_task_input):
        pass
