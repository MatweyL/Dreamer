from typing import Optional, List, Union

from server.domain.schemas.task import TaskTypePK, TaskType
from server.ports.outbound.repository.abstract import DOMAIN_MODEL, DOMAIN_MODEL_PK, DOMAIN_MODEL_INPUT, DomainEntityMapper
from server.ports.outbound.repository.domain.task import AbstractTaskTypeRepository
from server.ports.outbound.repository.queries import FilterFields, PaginationQuery


class MockTaskTypeRepository(AbstractTaskTypeRepository):

    def __init__(self, domain_mapper: DomainEntityMapper[TaskType, TaskType, TaskTypePK]):
        super().__init__(domain_mapper)

    async def create(self, domain_model_input: DOMAIN_MODEL_INPUT) -> DOMAIN_MODEL:
        pass

    async def get(self, domain_model_pk: DOMAIN_MODEL_PK) -> Optional[DOMAIN_MODEL]:
        pass

    async def update(self, domain_model: DOMAIN_MODEL) -> DOMAIN_MODEL:
        pass

    async def delete(self, domain_model_pk: DOMAIN_MODEL_PK) -> Optional[DOMAIN_MODEL]:
        pass

    async def paginated(self, pagination_query: PaginationQuery) -> List[DOMAIN_MODEL]:
        pass

    async def filter(self, filter_fields: FilterFields) -> List[DOMAIN_MODEL]:
        pass

    async def count_by_fields(self, filter_fields: FilterFields) -> int:
        pass
