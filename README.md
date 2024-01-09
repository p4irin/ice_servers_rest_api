[![My Skills](https://skillicons.dev/icons?i=py,flask)](https://skillicons.dev)
# ICE servers REST API - v1.0.0

A REST API to retrieve ICE servers, i.e. STUN and TURN servers, for use in WebRTC clients. TURN servers acquired from the API include ephemeral credentials as described in [A REST API For Access To TURN Services](https://datatracker.ietf.org/doc/html/draft-uberti-behave-turn-rest-00).

The API is for _application servers_ that serve a WebRTC client to its users. An application server uses it own authentication sub system to login users. When a user logs in it is served a WebRTC client along with the ICE servers it needs to traverse NATs. The ICE servers are retrieved from the API. Application servers authenticate to the API using an API key/token.

The list of ICE servers is served from a Python dict. So, _for a small number of ICE servers you should be ok. A simple and small setup_. If you want or have a larger set of ICE servers you want to selectively allot to specific application servers in a large set based on geo location etc, you should rely on a database to store and structure data related to ICE servers.

## API resource

There's only one resource which is "_read only_": ice-servers. The URL endpoint for this resource is `/ice-servers/` and only accepts an HTTP GET. You can specify a username query parameter: `/ice-servers/?username=JohnDoe`. This is optional but recommended as you can use it to correlate TURN server log entries to your application server log(s).

## Stack

- Python 3.8.10
- Ubuntu 20.04.2 LTS
  - curl

## Install

### From GitHub

```bash
(venv) $ pip install "git+https://github.com/p4irin/ice-servers-rest-api.git"
(venv) $
```
### Verify

1. Import and check the package version in a REPL
1. Run with Flask's development server
1. Test requesting an example list of configured ICE servers
    - with _curl_
    - or _httpie_

#### In a REPL

```BASH
(venv) $ python
Python 3.8.10 (default, Jun  2 2021, 10:49:15) 
[GCC 9.4.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import ice_servers_rest_api
>>> ice_servers_rest_api.__version__
'1.0.0'
>>>
```
There should be no errors when importing.

#### Run the API with Flask's development server

```bash
(venv) $ flask --app ice_servers_rest_api run
 * Serving Flask app 'ice_servers_rest_api'
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
```

With the API runnning on Flask's development server, you can now request an example list of STUN and TURN servers.

#### Use _curl_ to get the list of example ICE servers

On Ubuntu 20.04.2 LTS, _curl_ should be installed by default. If that's not the case, run

```bash
(venv) $ sudo apt install curl
```

and then get a list of configured ICE servers

```bash
(venv) $ curl \
> -v \
> -L \
> -H 'Authorization: Bearer Az96nia9oV7suDhWd2Zz5hS1iJfM1HYPxRn_rIeW9tY' \
> http://localhost:5000/ice-servers/?username=JohnDoe
*   Trying 127.0.0.1:5000...
* TCP_NODELAY set
* Connected to localhost (127.0.0.1) port 5000 (#0)
> GET /ice-servers/?username=JohnDoe HTTP/1.1
> Host: localhost:5000
> User-Agent: curl/7.68.0
> Accept: */*
> Authorization: Bearer Az96nia9oV7suDhWd2Zz5hS1iJfM1HYPxRn_rIeW9tY
> 
* Mark bundle as not supporting multiuse
< HTTP/1.1 200 OK
< Server: Werkzeug/3.0.0 Python/3.8.10
< Date: Sun, 15 Oct 2023 18:33:50 GMT
< Content-Type: application/json
< Content-Length: 405
< Connection: close
< 
[
  {
    "urls": "stun:stunserver1.example.com:3478"
  },
  {
    "urls": "stun:stunserver2.example.com:80"
  },
  {
    "credential": "V6nl2h1/3s3t8SWDpShuOdyR8sY=",
    "urls": "turn:turnserver1.example.com:3478",
    "username": "1697481230:JohnDoe"
  },
  {
    "credential": "uhnVAgh8oxHs3WQaDOUhhy3eHEI=",
    "urls": "turns:turnserver2.example.com:443",
    "username": "1697481230:JohnDoe"
  }
]
* Closing connection 0
```

```
-v shows raw HTTP request and response and curl feedback
-L follows redirections
-H Set the Authorization: header with the token/API-key
```
#### Or, use _httpie_

Install _httpie_

```bash
(venv) $ pip install httpie
```

Get a list of configured ICE servers

```bash
(venv) $ http \
> -A bearer \
> -a Az96nia9oV7suDhWd2Zz5hS1iJfM1HYPxRn_rIeW9tY \
> -v \
> http://localhost:5000/ice-servers/ username==JohnDoe
GET /ice-servers/?username=JohnDoe HTTP/1.1
Accept: */*
Accept-Encoding: gzip, deflate
Authorization: Bearer Az96nia9oV7suDhWd2Zz5hS1iJfM1HYPxRn_rIeW9tY
Connection: keep-alive
Host: localhost:5000
User-Agent: HTTPie/3.2.2



HTTP/1.1 200 OK
Connection: close
Content-Length: 405
Content-Type: application/json
Date: Sun, 15 Oct 2023 18:38:21 GMT
Server: Werkzeug/3.0.0 Python/3.8.10

[
    {
        "urls": "stun:stunserver1.example.com:3478"
    },
    {
        "urls": "stun:stunserver2.example.com:80"
    },
    {
        "credential": "Azyf6Y73ZWdOoKOBEpx0+/AdWYM=",
        "urls": "turn:turnserver1.example.com:3478",
        "username": "1697481501:JohnDoe"
    },
    {
        "credential": "OYDKc9oh+pZ4jNKUrcgGuahNa+w=",
        "urls": "turns:turnserver2.example.com:443",
        "username": "1697481501:JohnDoe"
    }
]
```

## Usage

Flask has a [reference](https://flask.palletsprojects.com/en/3.0.x/deploying/) for deployment options. The general approach is running a WSGI server behind a reverse proxy.

By default the API serves a list of example ICE servers.
To serve your own ICE servers specify them in `config.py` in the _instance_ directory. The application servers are also configured in `config.py`.

The format for configuring ICE and application servers in `config.py` is as follows:

```python
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
```

Use the above as an example to craft your own configuration.
A TURN server's `shared_secret` is used to generate ephemeral credentials. The application's `api_key` can be generated as follows

```bash
(venv) $ python -c 'import secrets; print(secrets.token_urlsafe())'
```

## Reference

- [A REST API For Access To TURN Services](https://datatracker.ietf.org/doc/html/draft-uberti-behave-turn-rest-00)
- [RFC 5766. Traversal Using Relays around NAT (TURN):Relay Extensions to Session Traversal Utilities for NAT (STUN)](https://datatracker.ietf.org/doc/html/rfc5766)
- [RFC 5389, Session Traversal Utilities for NAT (STUN)](https://datatracker.ietf.org/doc/html/rfc5389#section-10.2)
- [Flask](https://flask.palletsprojects.com/en/3.0.x/)
- [Flask-HTTPAuth](https://flask-httpauth.readthedocs.io/en/latest/)
- [Gunicorn](https://gunicorn.org/)
- [curl](https://curl.se/docs/manpage.html)
- [httpie](https://httpie.io/)
