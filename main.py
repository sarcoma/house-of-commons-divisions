from flask_cors import CORS

from app import create_app

app = create_app('flask.cfg')

CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}}, supports_credentials=True)
