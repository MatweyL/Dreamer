import re
from datetime import datetime
from uuid import uuid4

from sqlalchemy import MetaData, UUID, DateTime, func
from sqlalchemy.orm import mapped_column, Mapped, declared_attr, registry


def camel_to_snake(string: str):
    return re.sub(r'(?<!^)(?=[A-Z])', '_', string).lower()


naming_convention = {
    "all_column_names": lambda constraint, table: "_".join([column.name for column in constraint.columns.values()]),
    "ix": "ix_%(table_name)s_%(all_column_names)s",
    "uq": "uq_%(table_name)s_%(all_column_names)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(all_column_names)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

metadata = MetaData(naming_convention=naming_convention)
mapper_registry = registry(metadata=metadata)

Base = mapper_registry.generate_base()


class TablenameMixin:
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return camel_to_snake(cls.__name__)


class UUIDMixin:
    uid: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)


class LoadTimestampMixin:
    load_timestamp: Mapped[datetime] = mapped_column(DateTime, default=func.now())
