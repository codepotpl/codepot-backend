import jsonschema
from jsonschema import ValidationError
from rest_framework.parsers import JSONParser

from app.logging import logger
from app.views.exceptions import ParseException


class JSONSchemaParser(JSONParser):
    def __init__(self, schema):
        self.schema = schema

    def parse(self, stream, media_type=None, parser_context=None):
        data = super(JSONSchemaParser, self).parse(stream, media_type, parser_context)
        try:
            jsonschema.validate(data, self.schema)
            return data
        except ValidationError as e:
            logger.error('Caught JSON schema validation error: {}.'.format(str(e)))
            raise ParseException(str(e))


def parser_class_for_schema(schema):
    class X(JSONSchemaParser):
        def __init__(self):
            super(X, self).__init__(schema)
    return X