import os
from pathlib import Path


def get_project_root() -> Path:
    return Path(__file__).parent.parent.parent


def get_env_path():
    return os.path.join(get_project_root(), ".env")


def get_db_url(host: str, port: int, user: str, password: str, db_name: str):
    return f'postgresql+asyncpg://{user}:{password}@{host}:{port}/{db_name}'

def get_rabbit_dsn(
        protocol: str,
        user: str,
        password: str,
        host: str,
        port: str,
        virtual_host: str
):
    host = f"{host}:{port}" if port else host
    connection_url = f"{protocol}://{user}:{password}@{host}/{virtual_host}"
    return connection_url
