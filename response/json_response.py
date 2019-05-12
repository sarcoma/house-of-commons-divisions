import json
from functools import wraps

from flask import Response

from utilities.alchemy_encoder import AlchemyEncoder


def json_response(func):
    @wraps(func)
    def wrapped_function(**kwargs):
        return Response(
            response=json.dumps(func(**kwargs), cls=AlchemyEncoder),
            mimetype='application/json'
        )

    return wrapped_function
