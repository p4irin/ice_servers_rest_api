"""
"""


__author__ = 'p4irin'
__email__ = '139928764+p4irin@users.noreply.github.com'
__version__ = '1.0.0'


import os
from flask import Flask
from .ice_servers import bp as bp_ice_servers

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        STUN_URLS=[
            'stun:stunserver1.example.com:3478',
            'stun:stunserver2.example.com:80',
        ],
        TURN_SERVERS=[
            {
                'url': 'turn:turnserver1.example.com:3478',
                'shared_secret': 'Shared secret 1'
            },
            {
                'url': 'turns:turnserver2.example.com:443',
                'shared_secret': 'Shared secret 2'
            }
        ],
        APPLICATION_SERVERS=[
            {
                'description': 'aplication server 1',
                'api_key': 'FSSKOiMDIzXUPRjF2zxLKbtJlLsuxBoKqCpmX17kURc'
            },
            {
                'description': 'aplication server 2',
                'api_key': 'Az96nia9oV7suDhWd2Zz5hS1iJfM1HYPxRn_rIeW9tY'
            }            
        ]
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    app.register_blueprint(bp_ice_servers)

    return app