from flask import Blueprint, current_app, request
from .auth import token_auth
from turn_ephemeral_credentials import generate

bp = Blueprint('ice-servers', __name__, url_prefix='/ice-servers')

@bp.route("/", methods=['GET'])
@token_auth.login_required
def ice_servers():
    username = request.args.get(key='username', type=str)
    ice_servers = []
    for url in current_app.config['STUN_URLS']:
        ice_servers.append(
            {
                'urls': url
            }
        )
    for server in current_app.config['TURN_SERVERS']:
        credentials = generate(
            username,
            shared_secret=server['shared_secret']
        )        
        ice_servers.append(
            {
                'urls': server['url'],
                'username': credentials['turn_username'],
                'credential': credentials['turn_password']
            }
        )
    return ice_servers
