from flask_cors import CORS

from commons_divisions.app import create_app

if __name__ == '__main__':
    app = create_app('flask.cfg')

    CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}}, supports_credentials=True)
