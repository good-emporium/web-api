class BaseError(Exception):
    """Base Error Class"""

    def __init__(self, code=400, message=''):
        Exception.__init__(self)
        self.statusCode = code
        self.message = message

    def to_dict(self):
        return {'code': self.statusCode,
                'message': self.message}

class NotFoundError(BaseError):
    def __init__(self, message='Not found'):
        BaseError.__init__(self)
        self.statusCode = 404
        self.message = message

class CreateRecordError(BaseError):
    def __init__(self, message='Error in creating record'):
        BaseError.__init__(self)
        self.statusCode = 400
        self.message = message
