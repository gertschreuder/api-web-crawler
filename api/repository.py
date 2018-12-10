import pymongo


class Repository(object):

    def __init__(self, uri):
        self.maxWriteBatchSize = 100000
        self.db = pymongo.MongoClient(uri).leadbook

    def batchInsert(self, items):
        try:
            self.db.company.insert_many(items)
            return True
        except Exception as ex:
            print(ex)
            return False