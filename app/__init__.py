import jsonschema
from jsonschema import ValidationError
from rest_framework.parsers import JSONParser


class JSONSchemaParser(JSONParser):
    def __init__(self, schema):
        self.schema = schema

    def parse(self, stream, media_type=None, parser_context=None):
        data = super(JSONSchemaParser, self).parse(stream, media_type, parser_context)
        try:
            jsonschema.validate(data, self.schema)
            return data
        except ValidationError as e:
            print(str(e))
            raise e
            # TODO
            # log_and_raise(e.message, ParseError)


def parser_class_for_schema(schema):
    class X(JSONSchemaParser):
        def __init__(self):
            super(X, self).__init__(schema)
    return X


class CodepotException(Exception):
    def __init__(self, detail=None, code=0):
        self.detail = detail or 'No details'
        self.code = code


class BadRequestException(CodepotException):
    pass


class ForbiddenException(CodepotException):
    pass


# def log_and_raise(message, exc_class):
# logger.error(message)
#     raise exc_class(message)
