from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Optional, List, Type

from pydantic import BaseModel

from server.ports.outbound.repository.queries import FilterFields, PaginationQuery, UpdateFields

DOMAIN_MODEL_INPUT = TypeVar('DOMAIN_MODEL_INPUT', bound=BaseModel)
DOMAIN_MODEL = TypeVar('DOMAIN_MODEL', bound=BaseModel)
DOMAIN_MODEL_PK = TypeVar('DOMAIN_MODEL_PK', bound=BaseModel)

ENTITY_MODEL = TypeVar('ENTITY_MODEL')


class AbstractDomainEntityMapper(Generic[DOMAIN_MODEL, DOMAIN_MODEL_INPUT, DOMAIN_MODEL_PK]):

    def __init__(self, domain_model_input_class: Type[DOMAIN_MODEL_INPUT],
                 domain_model_class: Type[DOMAIN_MODEL],
                 domain_model_pk_class: Type[DOMAIN_MODEL_PK],
                 entity_model_class: Type[ENTITY_MODEL]):
        self._domain_model_input_class = domain_model_input_class
        self._domain_model_class = domain_model_class
        self._domain_model_pk_class = domain_model_pk_class
        self._entity_model_class = entity_model_class

    def domain_model_input(self, obj) -> DOMAIN_MODEL_INPUT:
        if isinstance(obj, self._domain_model_input_class):
            return obj
        return self._domain_model_input_class.model_validate(obj)

    def domain_model(self, obj) -> DOMAIN_MODEL:
        if isinstance(obj, self._domain_model_class):
            return obj
        return self._entity_to_domain_model(obj)

    def domain_model_pk(self, obj) -> DOMAIN_MODEL_PK:
        if isinstance(obj, self._domain_model_pk_class):
            return obj
        return self._domain_model_pk_class.model_validate(obj)

    @abstractmethod
    def _entity_to_domain_model(self, obj: Type[ENTITY_MODEL]):
        pass

    @abstractmethod
    def entity_model(self, obj) -> ENTITY_MODEL:
        pass


class AbstractRepository(Generic[DOMAIN_MODEL, DOMAIN_MODEL_INPUT, DOMAIN_MODEL_PK], ABC):

    def __init__(self, domain_mapper: AbstractDomainEntityMapper):
        self._domain_mapper = domain_mapper

    @abstractmethod
    async def create(self, domain_model_input: DOMAIN_MODEL_INPUT) -> DOMAIN_MODEL:
        raise NotImplementedError

    @abstractmethod
    async def get(self, domain_model_pk: DOMAIN_MODEL_PK) -> Optional[DOMAIN_MODEL]:
        raise NotImplementedError

    @abstractmethod
    async def update(self, domain_model_pk: DOMAIN_MODEL_PK, update_fields: UpdateFields) -> DOMAIN_MODEL:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, domain_model_pk: DOMAIN_MODEL_PK) -> Optional[DOMAIN_MODEL]:
        raise NotImplementedError

    @abstractmethod
    async def paginated(self, pagination_query: PaginationQuery) -> List[DOMAIN_MODEL]:
        raise NotImplementedError

    @abstractmethod
    async def filter(self, filter_fields: FilterFields) -> List[DOMAIN_MODEL]:
        raise NotImplementedError

    @abstractmethod
    async def count_by_fields(self, filter_fields: FilterFields) -> int:
        raise NotImplementedError
