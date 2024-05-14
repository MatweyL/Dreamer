from abc import ABC
from typing import Type

from pydantic import BaseModel


class Endpoint(ABC):

    async def execute(self, request: Type[BaseModel]) -> Type[BaseModel]:
        raise NotImplementedError
