import json
from pathlib import Path
from typing import List, Optional, Type, Dict

from server.adapters.outbound.repository.orm_sqlalchemy.base import Base
from server.ports.outbound.repository.abstract import AbstractRepository, DOMAIN_MODEL, DOMAIN_MODEL_PK, \
    DOMAIN_MODEL_INPUT, ENTITY_MODEL
from server.ports.outbound.repository.queries import FilterFields, PaginationQuery, UpdateFields


class AbstractJSONRepository(AbstractRepository):

    def __init__(self, domain_model_class: Type[DOMAIN_MODEL], domain_model_pk_class: Type[DOMAIN_MODEL_PK],
                 entity_model_class: Type[Base], path_to_json: Path):
        super().__init__(domain_model_class, domain_model_pk_class, entity_model_class)
        self._path_to_json = path_to_json
        self._data: Dict[DOMAIN_MODEL_PK, DOMAIN_MODEL] = {}
        if self._path_to_json.exists():
            self._data: Dict[DOMAIN_MODEL_PK, DOMAIN_MODEL] = json.loads(self._path_to_json.read_text('utf-8'))

    def _save_data(self):
        self._path_to_json.write_text(json.dumps(self._data, default=str))

    def entity_model(self, obj: DOMAIN_MODEL) -> ENTITY_MODEL:
        return obj.model_dump()

    def domain_model(self, obj: ENTITY_MODEL) -> DOMAIN_MODEL:
        return self._domain_model_class(**obj)

    def domain_model_pk(self, obj) -> DOMAIN_MODEL_PK:
        pk: Type[DOMAIN_MODEL_PK] = self._domain_model_pk_class(**obj.model_dump())
        return tuple(pk.model_dump().values())

    async def create(self, domain_model_input: DOMAIN_MODEL_INPUT) -> DOMAIN_MODEL:
        entity_model = self.entity_model(domain_model_input)
        pk = self.domain_model_pk(domain_model_input)
        self._data[pk] = entity_model
        self._save_data()
        return domain_model_input

    async def get(self, domain_model_pk: DOMAIN_MODEL_PK) -> Optional[DOMAIN_MODEL]:
        valid_domain_model_pk = self.domain_model_pk(domain_model_pk)

        entity_model = self._data.get(valid_domain_model_pk)
        if not entity_model:
            return None
        domain_model = self.domain_model(entity_model)
        return domain_model

    async def update(self, domain_model_pk: DOMAIN_MODEL_PK, update_fields: UpdateFields) -> DOMAIN_MODEL:
        valid_domain_model_pk = self.domain_model_pk(domain_model_pk)
        entity_model = await self.get(valid_domain_model_pk)
        if not entity_model:
            return None
        for field in update_fields.group:
            if field.name in entity_model:
                entity_model[field.name] = field.value
        self._data[valid_domain_model_pk] = entity_model
        self._save_data()
        domain_model = self.domain_model(entity_model)
        return domain_model

    async def delete(self, domain_model_pk: DOMAIN_MODEL_PK) -> Optional[DOMAIN_MODEL]:
        valid_domain_model_pk = self.domain_model_pk(domain_model_pk)

        entity_model = await self.get(valid_domain_model_pk)
        if not entity_model:
            return None
        domain_model = self.domain_model(entity_model)
        self._data.pop(valid_domain_model_pk)
        self._save_data()
        return domain_model

    async def paginated(self, pagination: PaginationQuery) -> List[DOMAIN_MODEL]:
        raise NotImplementedError

    async def filter(self, filter_fields: FilterFields) -> List[DOMAIN_MODEL]:
        filtered = []
        for entity in self._data.values():
            try:
                is_suitable = True
                for field in filter_fields.group:
                    if field.value == entity[field.name]:
                        continue
                    else:
                        is_suitable = False
                        break
            except KeyError:
                pass
            else:
                if is_suitable:
                    filtered.append(self.domain_model(entity))
        return filtered

    async def filter_one(self, filter_fields: FilterFields) -> Optional[DOMAIN_MODEL]:
        domain_models = await self.filter(filter_fields)
        if domain_models:
            return domain_models[0]

    async def count_by_fields(self, filter_fields: FilterFields) -> int:
        count = 0
        for entity in self._data.values():
            try:
                is_suitable = True
                for field in filter_fields.group:
                    if field.value == entity[field.name]:
                        continue
                    else:
                        is_suitable = False
                        break
            except KeyError:
                pass
            else:
                if is_suitable:
                    count += 1
        return count
