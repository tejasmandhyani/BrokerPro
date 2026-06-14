import json
import os
from datetime import datetime
import requests

BASE_URL = "https://brokerpro-80ao.onrender.com"



TOKEN_FILE = os.path.join(
    os.path.dirname(__file__),
    "storage",
    "token.json"
)


def load_tokens():

    if not os.path.exists(TOKEN_FILE):
        return {}

    with open(TOKEN_FILE, "r") as f:
        return json.load(f)


def save_tokens(tokens):

    with open(TOKEN_FILE, "w") as f:
        json.dump(tokens, f)


def login(username, password):

    print("=" * 50)
    print("Generating token for:", username)

    response = requests.post(

        f"{BASE_URL}/api/token/",

        json={
            "username": username,
            "password": password
        }

    )

    print("Status:", response.status_code)
    print("Body:", response.text)

    if response.status_code != 200:
        return None

    tokens = response.json()

    print("Current token file:", load_tokens())

    all_tokens = load_tokens()

    all_tokens[username] = tokens

    print("After update:", all_tokens)

    save_tokens(all_tokens)

    print("Saved successfully")
    print("=" * 50)

    return tokens
def refresh_access_token(username):

    all_tokens = load_tokens()

    if username not in all_tokens:

        return None

    refresh = all_tokens[username]["refresh"]

    response = requests.post(

        f"{BASE_URL}/api/token/refresh/",

        json={
            "refresh": refresh
        }

    )

    if response.status_code != 200:

        return None

    access = response.json()["access"]

    all_tokens[username]["access"] = access

    save_tokens(all_tokens)

    return access

def get_access_token(username):

    all_tokens = load_tokens()

    if username not in all_tokens:

        return None

    access = all_tokens[username]["access"]

    response = requests.get(

        f"{BASE_URL}/api/dashboard/properties/",

        headers={
            "Authorization": f"Bearer {access}"
        }

    )

    if response.status_code != 401:

        return access

    print("Access token expired. Refreshing...")

    access = refresh_access_token(username)

    if access:

        return access

    return None