from abc import ABC
from typing import List, Optional, Type

from sqlalchemy import select, desc, inspect, delete, update, func

from server.adapters.outbound.repository.orm_sqlalchemy.base import Base
from server.adapters.outbound.repository.orm_sqlalchemy.unit_of_work import UnitOfWork
from server.ports.outbound.repository.abstract import AbstractRepository, DOMAIN_MODEL, DOMAIN_MODEL_PK, \
    DOMAIN_MODEL_INPUT
from server.ports.outbound.repository.queries import FilterFields, PaginationQuery, UpdateFields


class AbstractSQLAlchemyRepository(AbstractRepository, ABC):
    
    def __init__(self, domain_model_class: Type[DOMAIN_MODEL], domain_model_pk_class: Type[DOMAIN_MODEL_PK],
                 entity_model_class: Type[Base], unit_of_work: UnitOfWork):
        super().__init__(domain_model_class, domain_model_pk_class, entity_model_class)
        self._uow = unit_of_work
        
    async def create(self, domain_model_input: DOMAIN_MODEL_INPUT) -> DOMAIN_MODEL:
        async with self._uow as uow:
            entity_model = self.entity_model(domain_model_input)
            uow.session.add(entity_model)
            await uow.commit()
            domain_model = self.domain_model(entity_model)
            return domain_model

    async def get(self, domain_model_pk: DOMAIN_MODEL_PK) -> Optional[DOMAIN_MODEL]:
        async with self._uow as uow:
            valid_domain_model_pk = self.domain_model_pk(domain_model_pk)
            query = select(self._entity_model_class).filter_by(**valid_domain_model_pk.model_dump())
            entity_model = await uow.session.scalar(query)
            if not entity_model:
                return None
            domain_model = self.domain_model(entity_model)
            return domain_model

    async def update(self, domain_model_pk: DOMAIN_MODEL_PK, update_fields: UpdateFields) -> DOMAIN_MODEL:
        async with self._uow as uow:
            valid_domain_model_pk = self.domain_model_pk(domain_model_pk)
            query = (update(self._entity_model_class).filter_by(**valid_domain_model_pk.model_dump())
                     .values(**update_fields.dict())).returning(self._entity_model_class)
            entity_model = await uow.session.scalar(query)
            await uow.commit()
            if not entity_model:
                return None
            domain_model = self.domain_model(entity_model)
            return domain_model

    async def delete(self, domain_model_pk: DOMAIN_MODEL_PK) -> Optional[DOMAIN_MODEL]:
        async with self._uow as uow:
            valid_domain_model_pk = self.domain_model_pk(domain_model_pk)
            query = (delete(self._entity_model_class)
                     .filter_by(**valid_domain_model_pk.model_dump())
                     .returning(self._entity_model_class))
            entity_model = await uow.session.scalar(query)
            await uow.commit()
            if not entity_model:
                return None
            domain_model = self.domain_model(entity_model)
            return domain_model

    async def paginated(self, pagination: PaginationQuery) -> List[DOMAIN_MODEL]:
        async with self._uow as uow:
            query = select(self._entity_model_class)
            if pagination.order_by:
                ordering_field_exists: bool = pagination.order_by in [column.key for column in
                                                                      inspect(self._entity_model_class).columns]
                if pagination.order_by and ordering_field_exists:
                    order_expression = getattr(self._entity_model_class, pagination.order_by)

                    if not pagination.asc_sort:
                        order_expression = desc(order_expression)
                    query = select(self._entity_model_class).order_by(order_expression)

                else:
                    raise Exception("Specified field 'order_by' doesn't exist")
            if pagination.limit_per_page is not None:
                query = query.limit(pagination.limit_per_page)
                if pagination.offset_page:
                    query = query.offset((pagination.offset_page - 1) * pagination.limit_per_page)
            if pagination.filter_fields:
                query = query.filter_by(**pagination.filter_fields.dict())

            entity_models = await uow.session.scalars(query)
            return [self.domain_model(entity_model) for entity_model in entity_models]

    async def filter(self, filter_fields: FilterFields) -> List[DOMAIN_MODEL]:
        async with self._uow as uow:
            query = select(self._entity_model_class).filter_by(**filter_fields.dict())
            entity_models = await uow.session.scalars(query)
            return [self.domain_model(entity_model) for entity_model in entity_models]

    async def count_by_fields(self, filter_fields: FilterFields) -> int:
        async with self._uow as uow:
            query = select(func.count()).select_from(self._entity_model_class)
            query = query.filter_by(**filter_fields.dict())
            count = await uow.session.scalar(query)

            return count
