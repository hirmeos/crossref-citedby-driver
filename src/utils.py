from os import environ
import sys

import requests


AUTH = None
AUTH_API_ENDP = environ['AUTH_API_ENDP']
JWT_DISABLED = environ['JWT_DISABLED'].lower() == 'true'
URI_API_ENDP = environ['URI_API_ENDP']
URI_API_USER = environ['URI_API_USER']
URI_API_PASS = environ['URI_API_PASS']
URI_SCHEME = environ['URI_SCHEME']
URI_STRICT = environ['URI_STRICT']


def get_token(url, email, passwd):
    """Fetch token from tokens API."""
    credentials = {'email': email, 'password': passwd}
    res = requests.post(url, json=credentials)

    try:
        assert res.status_code == 200
    except AssertionError:
        raise ValueError(res.content.decode('utf-8'))

    return res.json()['data'][0]['token']


def doi_to_id(doi, timestamp):
    """Query translator to convert book DOI to specified schema."""
    params = {
        'uri': doi,
        'filter': f'uri_scheme:{URI_SCHEME}',
        'strict': URI_STRICT
    }

    headers = {'Authorization': AUTH} if AUTH else {}

    response = requests.get(URI_API_ENDP, params=params, headers=headers)

    try:
        assert response.status_code == 200
    except AssertionError:
        r = response.json()
        print(
            f"{r['message']}: {r['parameters']['uri']} ({timestamp})",
            file=sys.stderr
        )
        return []

    return response.json()['data']


def set_token_auth():
    """Set authorisation header for JWT token using the Bearer schema."""

    global AUTH

    if not JWT_DISABLED:
        api_jwt = get_token(AUTH_API_ENDP, URI_API_USER, URI_API_PASS)
        AUTH = f'Bearer {api_jwt}'
