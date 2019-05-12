from flask import json
from flask.json import JSONEncoder
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.orm.collections import InstrumentedList


class AlchemyEncoder(JSONEncoder):

    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                if isinstance(data, InstrumentedList):
                    data = [self.default(row) for row in data]
                try:
                    json.dumps(data)
                    fields[field] = data
                except TypeError:
                    pass

            return fields

        return json.JSONEncoder.default(self, obj)
