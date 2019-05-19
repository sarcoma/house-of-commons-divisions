
from flask import json
from flask.json import JSONEncoder


class ListAlchemyEncoder(JSONEncoder):
    def default(self, o):
        return json.JSONEncoder.default(self, o)


class DetailAlchemyEncoder(JSONEncoder):
    def default(self, o):
        return json.JSONEncoder.default(self, o)
