import sys
import logging

from flask_cors import CORS

directory = "/var/www/site_dir"

logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, "%s/commons_divisions" % directory)

activate_this = "%s/venv/bin/activate_this.py" % directory
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))


from commons_divisions.app import create_app

app = create_app("%s/flask.cfg"  % directory)

CORS(app, resources={r"/*": {"origins": ["http://localhost:3000","https://commonsdivisions.orderandchaoscreative.com"]}}, supports_credentials=True)

application = app
