from codepot.models import (
    TicketTypeName,
    PurchaseTypeName,
)

make_purchase_req_schema = {
    '$schema': 'http://json-schema.org/draft-04/schema',
    'type': 'object',
    'properties': {
        'promoCode': {
            'type': ['string', 'null', ],
            'minLength': 1,
            'pattern': '^[A-Z0-9]{6}$',
        },
        'ticketType': {
            'enum': [t.value for t in TicketTypeName]
        },
        'purchaseType': {
            'enum': [t.value for t in PurchaseTypeName]
        },
        'invoice': {
            'type': ['object', 'null', ],
            'properties': {
                'name': {
                    'type': 'string',
                    'minLength': 1,
                },
                'street': {
                    'type': 'string',
                    'minLength': 1,
                },
                'zipCode': {
                    'type': 'string',
                    'minLength': 1,
                    'pattern': '^\d{2}-\d{3}$',
                },
                'taxId': {
                    'type': 'string',
                    'minLength': 1,
                    'pattern': '^[0-9]{10}$',
                },
                'country': {
                    'type': 'string',
                    'minLength': 1,
                },
            },
            'required': ['name', 'street', 'zipCode', 'taxId', 'country', ],
            'additionalProperties': False,
        },
    },
    'required': ['promoCode', 'ticketType', 'purchaseType', 'invoice', ],
    'additionalProperties': False,
}
