from flask import json
from flask.json import JSONEncoder
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.orm.collections import InstrumentedList

from models.member_of_parliament import MemberOfParliament


class AlchemyEncoder(JSONEncoder):

    def default(self, obj, level=0):
        if isinstance(obj.__class__, DeclarativeMeta):
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                data = self.handle_nested_list(data, level)
                try:
                    json.dumps(data)
                    fields[field] = data
                except TypeError:
                    pass

            return fields

        return json.JSONEncoder.default(self, obj)

    def handle_nested_list(self, data, level):
        if isinstance(data, InstrumentedList) and level < 2:
            data = [self.default(row, level + 1) for row in data]
        return data
