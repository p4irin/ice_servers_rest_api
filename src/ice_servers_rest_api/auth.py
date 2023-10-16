from flask_httpauth import HTTPTokenAuth
from flask import current_app
from .errors import error_response

token_auth = HTTPTokenAuth()

@token_auth.verify_token
def verify_token(token):
    for server in current_app.config['APPLICATION_SERVERS']:
        if server['api_key'] == token:
            return True
    return False

@token_auth.error_handler
def token_auth_error(status):
    return error_response(status)