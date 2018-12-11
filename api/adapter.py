from api.repository import Repository
from api.result import Result
import json
import os

class Adapter(object):
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger        
        self.database = Repository(config, logger)

    def getJsonDocument(self, path):
        basepath = os.path.dirname(__file__)
        abs_file_path = os.path.abspath(os.path.join(basepath, "..", path))
        with open(abs_file_path) as data:
            return json.load(data)

    def seed_database(self) -> bool:
        try:
            data = self.getJsonDocument('data\company_profiles.json')
            success = self.database.batchInsertCompanyData(data)
            return success
        except Exception as ex:
            self.logger.error(ex)
            return False

    def getCompanies(self, name:str=None):
        companies = []
        try:
            if name is None:
                companies = self.database.getCompanies()
            else:
                companies = self.database.getCompaniesBy(name)
            return Result('200', 'successful', companies)
        except Exception as ex:
            self.logger.error(ex)
            return Result('400', 'An Error Occurred.', [])