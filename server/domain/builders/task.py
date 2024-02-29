from server.domain.interfaces import FullTaskBuilderInterface
from server.domain.schemas import TaskPK
from server.domain.schemas.full import FullTask
from server.ports.outbound.repository.domain.pipeline import AbstractTaskDataTemplateRepository
from server.ports.outbound.repository.domain.task import AbstractTaskRepository, AbstractTaskDataRepository, \
    AbstractTaskTypeRepository
from server.ports.outbound.repository.queries import FilterFields, Field


class TaskFullBuilder(FullTaskBuilderInterface):

    def __init__(self, task_repo: AbstractTaskRepository,
                 task_type_repo: AbstractTaskTypeRepository,
                 task_data_repo: AbstractTaskDataRepository,
                 task_data_template_repo: AbstractTaskDataTemplateRepository):
        self._task_repo = task_repo
        self._task_type_repo = task_type_repo
        self._task_data_repo = task_data_repo
        self._task_data_template_repo = task_data_template_repo

    async def build(self, task_pk: TaskPK) -> FullTask:
        task = await self._task_repo.get(task_pk)
        task_type = await self._task_type_repo.get(task.type)
        task_data_input = await self._task_data_repo.filter(FilterFields(group=[Field(name='task_uid', value=task.uid),
                                                                                Field(name='is_input', value=True)]))
        task_data_output = await self._task_data_repo.filter(FilterFields(group=[Field(name='task_uid', value=task.uid),
                                                                                 Field(name='is_input', value=False)]))
        data_output_template = await self._task_data_template_repo.filter(
            FilterFields(group=[Field(name='task_type_uid',
                                      value=task.type.uid),
                                Field(name='is_input', value=False)]))
        task_full = FullTask(uid=task.uid, status=task.status,
                             type=task_type, data_input=task_data_input,
                             data_output=task_data_output,
                             data_output_template=data_output_template)
        return task_full
