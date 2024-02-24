from sqlalchemy import Column, String

from server.adapters.outbound.repository.orm_sqlalchemy.base import Base, TablenameMixin, UUIDMixin, LoadTimestampMixin


class Pipeline(Base, TablenameMixin, UUIDMixin, LoadTimestampMixin):
    name = Column(String(128), nullable=False, unique=True)
