import pymongo


class Repository(object):

    def __init__(self, config, logger):

        self.config = config
        self.logger = logger

        dbConfig = self.config['DATABASES']
        if self.config['PRODUCTION']:
            host = dbConfig['docker']['HOST']
            port = dbConfig['docker']['PORT']
            database_name = dbConfig['docker']['NAME']
        else:
            host = dbConfig['local']['HOST']
            port = dbConfig['local']['PORT']
            database_name = dbConfig['local']['NAME']

        self.client = pymongo.MongoClient(host, port)
        self.db = self.client[database_name]
        self.collection = self.db['company']

    def batchInsertCompanyData(self, companyData):
        try:
            self.db.company.insert(companyData)
            return True
        except Exception as ex:
            self.logger.error(ex)
            return False

    def getCompanies(self, params):
        try:
            cursor = self.db.company.find(params)
            documents = [c for c in cursor]
            return documents
        except Exception as ex:
            self.logger.error(ex)
            return []
