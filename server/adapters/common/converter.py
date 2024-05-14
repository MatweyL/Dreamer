from typing import Type, Any

from pydantic import BaseModel

from server.ports.common import ConverterI


class StrToPydanticConverter(ConverterI):

    def __init__(self, schema: Type[BaseModel]):
        self._schema = schema

    def convert(self, data: str) -> Type[BaseModel]:
        return self._schema.model_validate_json(data)


class ChainedConverter(ConverterI):

    def __init__(self, current_converter: ConverterI, next_converter: ConverterI):
        self._current_converter = current_converter
        self._next_converter = next_converter

    def convert(self, data: Any) -> Any:
        try:
            result = self._current_converter.convert(data)
        except BaseException as e:
            if self._next_converter:
                return self._next_converter.convert(data)
            raise e
        else:
            return result
