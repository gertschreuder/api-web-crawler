import json
from bson.objectid import ObjectId


class JSONEncoder(json.JSONEncoder):
    # pylint: disable=E0202
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)
