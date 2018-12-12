class Result(object):
    def __init__(self, code, msg, data):
        self.status_code = code
        self.message = msg
        self.data = data
