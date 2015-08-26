from codepot.models import TimeSlotTierDayName

workshop_res_schema = {
  '$schema': 'http://json-schema.org/draft-04/schema',
  'type': 'object',
  'properties': {
    'id': {
      'type': 'integer',
    },
    'title': {
      'type': 'string',
      'minLength': 1,
    },
    'description': {
      'type': 'string',
      'minLength': 1,
    },
    'maxAttendees': {
      'type': 'integer',
    },
    'attendeesCount': {
      'type': 'integer',
    },
    'timeSlots': {
      'type': 'array',
      'uniqueItems': True,
      'minItems': 1,
      'items': {
        'type': 'object',
        'properties': {
          'id': {
            'type': 'string',
            'minLength': 1,
          },
          'day': {
            'enum': [t.value for t in TimeSlotTierDayName]
          },
          'startTime': {
            'type': 'string',
            'minLength': 1,
          },
          'endTime': {
            'type': 'string',
            'minLength': 1,
          },
          'room': {
            'type': 'string',
          },
          'order': {
            'type': 'integer',
            'minimum': 0,
          }
        },
        'required': ['id', 'day', 'startTime', 'endTime', 'room', 'order', ],
        'additionalProperties': False,
      },
    },
    'mentors': {
      'type': 'array',
      'uniqueItems': True,
      'minItems': 1,
      'items': {
        'type': 'object',
        'properties': {
          'id': {
            'type': 'integer',
            'minimum': 1,
          },
          'firstName': {
            'type': 'string',
            'minLength': 1,
          },
          'lastName': {
            'type': 'string',
            'minLength': 1,
          },
          'tagline': {
            'type': ['string', 'null'],
          },
          'pictureURL': {
            'type': ['string', 'null'],
          },
          'twitterUsername': {
            'type': ['string', 'null'],
          },
          'githubUsername': {
            'type': ['string', 'null'],
          },
          'linkedinProfileURL': {
            'type': ['string', 'null'],
          },
          'stackoverflowId': {
            'type': ['string', 'null'],
          },
          'googleplusHandler': {
            'type': ['string', 'null'],
          },
          'websiteURL': {
            'type': ['string', 'null'],
          },
          'bioInMd': {
            'type': ['string', 'null'],
          },
        },
        'required': ['id', 'firstName', 'lastName', 'tagline', 'pictureURL', 'twitterUsername', 'githubUsername',
                     'linkedinProfileURL', 'stackoverflowId', 'googleplusHandler', 'websiteURL', 'bioInMd'],
        'additionalProperties': False,
      },
    },
    'tags': {
      'type': 'array',
      'uniqueItems': True,
      'minItems': 1,
      'items': {
        'type': 'object',
        'properties': {
          'id': {
            'type': 'string',
            'minLength': 1,
          },
          'name': {
            'type': 'string',
            'minLength': 1,
          },
        },
        'required': ['id', 'name', ],
        'additionalProperties': False,
      },
    },
  },
  'required': ['id', 'title', 'description', 'maxAttendees', 'attendeesCount', 'timeSlots', 'mentors', 'tags', ],
  'additionalProperties': False,
}

workshops_list_res_schema = {
  '$schema': 'http://json-schema.org/draft-04/schema',
  'type': 'object',
  'properties': {
    'workshops': {
      'type': 'array',
      'uniqueItems': True,
      'items': workshop_res_schema,
    },
  },
  'required': ['workshops', ],
  'additionalProperties': False,
}

workshop_message_req_schema = {
  '$schema': 'http://json-schema.org/draft-04/schema',
  'type': 'object',
  'properties': {
    'content': {
      'type': 'string',
      'minLength': 1,
    },
  },
  'required': ['content', ],
  'additionalProperties': False,
}

workshop_message_res_schema = {
  '$schema': 'http://json-schema.org/draft-04/schema',
  'type': 'object',
  'properties': {
    'id': {
      'type': 'string',
      'minLength': 1,
    },
    'author': {
      'type': 'object',
      'properties': {
        'id': {
          'type': 'integer',
        },
        'firstName': {
      'type': 'string',
      'minLength': 1,
        },
        'lastName': {
          'type': 'string',
          'minLength': 1,
        },
      },
      'required': ['id', 'firstName', 'lastName', ],
      'additionalProperties': False,
    },
    'content': {
      'type': 'string',
      'minLength': 1,
    },
    'created': {
      'type': 'string',
      'minLength': 1,
    }
  },
  'required': ['id', 'author', 'created', 'content', ],
  'additionalProperties': False,
}

sign_for_workshop_req_schema = {
  '$schema': 'http://json-schema.org/draft-04/schema',
  'type': 'object',
  'properties': {
    'workshopId': {
      'type': 'integer',
    },
  },
  'required': ['workshopId', ],
  'additionalProperties': False,
}

workshop_search_req_schema = {
  '$schema': 'http://json-schema.org/draft-04/schema',
  'type': 'object',
  'properties': {
    'query': {
      'type': 'string',
      'minLength': 3,
    },
  },
  'required': ['query', ],
  'additionalProperties': False,
}

workshop_places_res_schema = {
  '$schema': 'http://json-schema.org/draft-04/schema',
  'type': 'object',
  'properties': {
    'places': {
      'type': 'array',
      'uniqueItems': True,
      'minItems': 1,
      'items': {
        'type': 'object',
        'properties': {
          'workshopId': {
            'type': 'integer',
          },
          'maxAttendees': {
            'type': 'integer',
          },
          'attendeesCount': {
            'type': 'integer',
          },
        },
        'required': ['workshopId', 'maxAttendees', 'attendeesCount', ],
        'additionalProperties': False,
      },
    },
  },
  'required': ['places', ],
  'additionalProperties': False,
}
