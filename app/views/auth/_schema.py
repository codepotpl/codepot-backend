sign_in_req_schema = {
    "$schema": "http://json-schema.org/draft-04/schema",
    "type": "object",
    "properties": {
        "email": {
            "type": "string",
            "minLength": 1,
            "format": "email",
        },
        "password": {
            "type": "string",
            "minLength": 1,
        },
    },
    "required": ["email", "password", ],
    "additionalProperties": False,
}

sign_up_req_schema = {
    "$schema": "http://json-schema.org/draft-04/schema",
    "type": "object",
    "properties": {
        "email": {
            "type": "string",
            "minLength": 1,
            "format": "email",
        },
        "password": {
            "type": "string",
            "minLength": 1,
        },
        "firstName": {
            "type": "string",
            "minLength": 1,
        },
        "lastName": {
            "type": "string",
            "minLength": 1,
        }

    },
    "required": ["email", "password", "firstName", "lastName"],
    "additionalProperties": False,
}