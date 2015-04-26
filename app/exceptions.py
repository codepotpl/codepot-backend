class CodepotException(Exception):
    def __init__(self, detail=None, code=0):
        self.detail = detail or 'No details'
        self.code = code


# def log_and_raise(message, exc_class):
# logger.error(message)
# raise exc_class(message)

