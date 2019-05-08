from datetime import datetime
from enum import Enum
from functools import singledispatch

from drone_squadron.transformer.transformer import Transformer


class JsonTransformer(Transformer):

    def __init__(self):
        self.get_data = singledispatch(self.get_data)
        self.get_data.register(list, self._handle_list)

    def get_data(self, data):
        dictionary = {}
        for key, field in data.items():
            field = self.convert_datetime_to_string(field)
            field = self.convert_enum(field)
            dictionary[key] = field
        return dictionary

    def _handle_list(self, data):
        result = []
        for item in data:
            result.append(self.get_data(item))
        return result

    def convert_datetime_to_string(self, field):
        if isinstance(field, datetime):
            field = field.strftime("%Y-%m-%d %H:%M:%S")
        return field

    def convert_enum(self, field):
        if isinstance(field, Enum):
            field = {field.name: field.value}
        return field
