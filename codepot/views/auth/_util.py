def prepare_auth_response_map(user):
    return {
        'headers': {
            'Token': user.auth_token.key
        },
        'data': {
            'id': user.id,
            'email': user.email,
            'firstName': user.first_name,
            'lastName': user.last_name,
        }
    }