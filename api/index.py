#!flask/bin/python
from flask import Flask

app = Flask(__name__)

@app.route('/companies', methods=['GET'])
def get_tasks():
    raise NotImplementedError

@app.route('/companies', methods=['GET'])
def get_companies_by(company_name=None, industry=None, revenue_gte=None):
    if company_name is not None:
        get_companies_by_company_name(company_name)
    elif industry is not None:
        get_companies_by_industry(industry)
    elif revenue_gte is not None:
        get_companies_by_revenue_gte(revenue_gte)
    else:
        raise NotImplementedError

def get_companies_by_company_name(company_name):
    raise NotImplementedError

def get_companies_by_industry(industry):
    raise NotImplementedError

def get_companies_by_revenue_gte(revenue_gte):
    raise NotImplementedError

if __name__ == '__main__':
    app.run(debug=True)