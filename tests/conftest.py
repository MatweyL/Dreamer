import pytest

from server.adapters.outbound.repository.orm_sqlalchemy.settings import settings
from server.adapters.outbound.repository.orm_sqlalchemy.unit_of_work import UnitOfWork


@pytest.fixture(scope='session')
def db_url():
    return settings.get_db_url(async_mode=True)


@pytest.fixture(scope='session')
def unit_of_work(db_url):
    return UnitOfWork(db_url=db_url)
