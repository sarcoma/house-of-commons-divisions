from flask import Flask, json

from models.commons_division import CommonsDivision
from orm.orm import session_factory
from utilities.alchemy_encoder import AlchemyEncoder

app = Flask(__name__)

session = session_factory()

@app.route('/')
def commons_division_list():
    data = session.query(CommonsDivision).all()

    return app.response_class(
        response=json.dumps(data, cls=AlchemyEncoder),
        mimetype='application/json'
    )


@app.route('/<int:commons_division_id>')
def commons_division_detail(commons_division_id):
    data = session.query(CommonsDivision).get(commons_division_id)

    return app.response_class(
        response=json.dumps(data, cls=AlchemyEncoder),
        mimetype='application/json'
    )


if __name__ == '__main__':
    app.run()
