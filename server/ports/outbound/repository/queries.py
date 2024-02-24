from dataclasses import dataclass
from typing import Optional, Any, List


@dataclass
class BasePagination:
    offset_page: Optional[int] = None
    limit_per_page: Optional[int] = None
    order_by: Optional[str] = None
    asc_sort: Optional[bool] = None


@dataclass
class Field:
    name: str
    value: Any

    def dict(self):
        return {self.name: self.value}


@dataclass
class FieldsGroup:
    group: List[Field] = None

    def dict(self):
        if self.group:
            return {field.name: field.value for field in self.group}
        return {}


@dataclass
class FilterFields(FieldsGroup):
    pass


@dataclass
class UpdateFields(FieldsGroup):
    pass


@dataclass
class PaginationQuery(BasePagination):
    filter_fields: FilterFields = None
