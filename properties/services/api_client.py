import requests
from urllib.parse import urlencode
from .token_manager import get_access_token

import os

BASE_URL = os.environ.get(
    "API_BASE_URL",
    "https://brokerpro-80ao.onrender.com"
)


def get(endpoint, params=None, auth=True):

    session = requests.Session()
    session.trust_env = False

    url = f"{BASE_URL}{endpoint}"

    if params:
        from urllib.parse import urlencode
        url += "?" + urlencode(params)

    headers = {}

    if auth:
        token = get_access_token()
        headers["Authorization"] = f"Bearer {token}"

    response = session.get(
        url,
        headers=headers
    )

    print("=" * 60)
    print("URL:", url)
    print("STATUS:", response.status_code)
    print("BODY:")
    print(response.text)
    print("=" * 60)

    response.raise_for_status()

    return response.json()
def get_property(id):

    return get(
        f"/api/properties/{id}/",
        auth=False
    )



def post(endpoint, data, auth=True):

    session = requests.Session()
    session.trust_env = False

    headers = {}

    if auth:
        token = get_access_token()
        headers["Authorization"] = f"Bearer {token}"

    response = session.post(
        f"{BASE_URL}{endpoint}",
        data=data,
        headers=headers
    )

    print("STATUS:", response.status_code)
    print("BODY:", response.text)

    return response.status_code

def put(endpoint, data, auth=True):

    session = requests.Session()
    session.trust_env = False

    headers = {}

    if auth:
        token = get_access_token()
        headers["Authorization"] = f"Bearer {token}"

    response = session.put(
        f"{BASE_URL}{endpoint}",
        data=data,
        headers=headers
    )

    return response.status_code


def delete(endpoint, auth=True):

    session = requests.Session()
    session.trust_env = False

    headers = {}

    if auth:
        token = get_access_token()
        headers["Authorization"] = f"Bearer {token}"

    response = session.delete(
        f"{BASE_URL}{endpoint}",
        headers=headers
    )

    return response.status_code

