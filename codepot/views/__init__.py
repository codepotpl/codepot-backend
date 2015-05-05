import jsonschema
from jsonschema import ValidationError
from rest_framework.parsers import JSONParser

from codepot.logging import logger
from codepot.views.exceptions import ParseException


class JSONSchemaParser(JSONParser):
    def __init__(self, schema):
        self.schema = schema

    def parse(self, stream, media_type=None, parser_context=None):
        data = super(JSONSchemaParser, self).parse(stream, media_type, parser_context)
        return validate_payload_with_schema(data, self.schema)


def validate_payload_with_schema(payload, schema):
    """
    Needed because of: https://github.com/tomchristie/django-rest-framework/issues/2556
    When empty request comes it's not parsed.
    """
    try:
        jsonschema.validate(payload, schema)
        return payload
    except ValidationError as e:
        logger.error('Caught JSON schema validation error: {}.'.format(str(e)))
        raise ParseException(str(e), 400)


def parser_class_for_schema(schema):
    class X(JSONSchemaParser):
        def __init__(self):
            super(X, self).__init__(schema)
    return X