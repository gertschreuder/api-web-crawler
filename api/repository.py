import pymongo


class Repository(object):

    def __init__(self, config, logger):
        
        self.config = config
        self.logger = logger

        dbConfig = self.config['DATABASES']
        if self.config['PRODUCTION']:
            host = dbConfig['prod']['HOST']
            port = dbConfig['prod']['PORT']
            database_name = dbConfig['prod']['NAME']
        else:
            host = dbConfig['dev']['HOST']
            port = dbConfig['dev']['PORT']
            database_name = dbConfig['dev']['NAME']

        self.maxWriteBatchSize = 100000
        self.client = pymongo.MongoClient(host=host, port=port)
        self.db = self.client[database_name]
        self.collection = self.db['company']

    def batchInsertCompanyData(self, companyData) -> bool:
        try:
            # TODO: check self.maxWriteBatchSize
            self.db.company.insert_many(companyData)
            return True
        except Exception as ex:
            self.logger.error(ex)
            return False

    def getCompanies(self):
        try:
            documents = self.db.company.find()
            return documents
        except Exception as ex:
            self.logger.error(ex)
            return None

    def getCompaniesBy(self, company_name: str):
        try:
            documents = self.db.company.find({"company name": company_name})
            return documents
        except Exception as ex:
            self.logger.error(ex)
            return None
