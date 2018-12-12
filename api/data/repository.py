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
            table = dbConfig['docker']['TABLE']
        else:
            host = dbConfig['local']['HOST']
            port = dbConfig['local']['PORT']
            database_name = dbConfig['local']['NAME']
            table = dbConfig['local']['TABLE']

        self.client = pymongo.MongoClient(host, port)
        self.db = self.client[database_name]
        self.collection = self.db[table]

    def batchInsertCompanyData(self, companyData):
        """
        Batch insert json collection of objects
        """
        try:
            if self.collection.find({}).count() > 0:
                self.collection.delete_many({})
            self.collection.insert(companyData)
            return True
        except Exception as ex:
            self.logger.error(ex)
            return False

    def getCompanies(self, params):
        """
        Retrieves one or many items from database depending on the inclusion of a filter parameter
        """
        try:
            cursor = self.collection.find(params)
            documents = [c for c in cursor]
            return documents
        except Exception as ex:
            self.logger.error(ex)
            return []
