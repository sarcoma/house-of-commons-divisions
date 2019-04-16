from functools import wraps

from flask import Flask, json

from models.commons_division import CommonsDivision
from models.member_of_parliament import MemberOfParliament
from orm.orm import session_factory
from utilities.alchemy_encoder import AlchemyEncoder

app = Flask(__name__)

session = session_factory()


# Todo: Add a nesting level to manage depth
# Todo: Handle serializing nested models
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
def route_list():
    return {'routes': ['/commons-division', '/member-of-parliament']}


@app.route('/commons-division')
@json_response
def commons_division_list():
    return session.query(CommonsDivision).all()


@app.route('/commons-division/<int:commons_division_id>')
@json_response
def commons_division_detail(commons_division_id):
    return session.query(CommonsDivision).get(commons_division_id)


@app.route('/member-of-parliament')
@json_response
def member_of_parliament_list():
    return session.query(MemberOfParliament).all()


@app.route('/member-of-parliament/<int:member_of_parliament_id>')
@json_response
def member_of_parliament_detail(member_of_parliament_id):
    return session.query(MemberOfParliament).get(member_of_parliament_id)


if __name__ == '__main__':
    app.run()
