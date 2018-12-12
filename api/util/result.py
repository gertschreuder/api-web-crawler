class Result(object):
    """
    API return object
    """
    def __init__(self, code: int, msg: str, data):
        self.status_code = code
        self.message = msg
        self.data = data
