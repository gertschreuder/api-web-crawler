#!flask/bin/python
from flask import Flask, request,jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import default_settings
import logging
import logging.handlers
from api.adapter import Adapter


app = Flask(__name__)
app.config.from_object(default_settings)
handler = logging.handlers.RotatingFileHandler(
        'app.log',
        maxBytes=1024 * 1024)
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
    return jsonify(result)

def seed_db():
    return service.seed_database()

if __name__ == '__main__':
    success = seed_db()
    if success:
        app.run(debug=app.config['PRODUCTION'], ssl_context='adhoc')
    else:
        print('Unable to seed database. Check if connection details are set in default_settings.')

