import json

from drone_squadron.error.error import Error
from drone_squadron.transformer.json_transformer import JsonTransformer


def json_response(data, status=200):
    if isinstance(data, Error):
        status = data.get_status_code()
        data = data.get_error()
    else:
        data = JsonTransformer().get_data(data)
    from drone_squadron.main import app
    response = app.response_class(
        response=json.dumps(data),
        status=status,
        mimetype='application/json'
    )

    return response
