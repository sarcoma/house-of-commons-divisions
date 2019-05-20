import json
from functools import wraps

from flask import Response
from flask.json import JSONEncoder


def json_response(func):
    @wraps(func)
    def wrapped_function(**kwargs):
        return Response(
            response=json.dumps(func(**kwargs), cls=JSONEncoder),
            mimetype='application/json'
        )

    return wrapped_function
