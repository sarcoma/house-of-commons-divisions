from functools import wraps

from flask import Flask, json

from models.commons_division import CommonsDivision
from orm.orm import session_factory
from utilities.alchemy_encoder import AlchemyEncoder

app = Flask(__name__)

session = session_factory()


def json_response(func):
    @wraps(func)
    def wrapped_function(*args, **kwargs):
        return app.response_class(
            response=json.dumps(func(**kwargs), cls=AlchemyEncoder),
            mimetype='application/json'
        )

    return wrapped_function


@app.route('/')
@json_response
def commons_division_list():
    data = session.query(CommonsDivision).all()

    return data


@app.route('/<int:commons_division_id>')
@json_response
def commons_division_detail(commons_division_id):
    data = session.query(CommonsDivision).get(commons_division_id)

    return data


if __name__ == '__main__':
    app.run()
