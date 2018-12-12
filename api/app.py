#!flask/bin/python
# pylint: disable=E0401,E0611,E1101
from flask import Flask, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import default_settings
import json
import logging
import logging.handlers
from adapter import Adapter
from util.jsonEncoder import JSONEncoder


app = Flask(__name__)
app.config.from_object(default_settings)
handler = logging.handlers.RotatingFileHandler('app.log', maxBytes=1024 * 1024)
handler.setLevel(logging.INFO)
app.logger.addHandler(handler)

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["1 per second"],
)

service = Adapter(app.config, app.logger)


@app.route("/ping")
@limiter.exempt
def ping():
    return 'PONG'


@app.route('/companies', methods=['GET'])
def get():
    company_name = request.args.get('company_name')
    result = service.getCompanies(company_name)
    return JSONEncoder().encode(result.__dict__)


def seed_db():
    return service.seed_database()

if __name__ == '__main__':
    success = seed_db()
    if success:
        app.run(host='0.0.0.0', debug=app.config['PRODUCTION'])  # , ssl_context='adhoc'
    else:
        print('Unable to seed database. Check if connection details are set in default_settings.')
