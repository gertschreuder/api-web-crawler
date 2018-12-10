#!flask/bin/python
from flask import Flask

app = Flask(__name__)


@app.route('/companies', methods=['GET'])
def get_companies_by(company_name: str=None):
    if company_name is None:
        get_companies_by_company_name(company_name)
    else:
        get_companies()


def get_companies():
    raise NotImplementedError


def get_companies_by_company_name(company_name: str):
    raise NotImplementedError

if __name__ == '__main__':
    app.run(debug=True)
