class CustomError(Exception):
    def __init__(self, message, cause):
        super(CustomError, self).__init__(message + u', caused by '+ repr(cause))
        self.cause = cause
try:
    {}['a']
except KeyError as ke:
    raise CustomError("Error", ke)
