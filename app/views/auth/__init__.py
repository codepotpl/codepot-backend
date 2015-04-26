from ._sign_in import sign_in
from ._sign_up import sign_up


def _prepare_auth_response_map(user):
    return {
        'headers': {
            'Token': user.auth_token.key
        },
        'data': {
            'id': user.id,
            'email': user.userprofile.email,
            'firstName': user.userprofile.first_name,
            'lastName': user.userprofile.last_name,
        }
    }