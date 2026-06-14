import json
import os
from datetime import datetime
import requests

BASE_URL = "https://brokerpro-80ao.onrender.com"

USERNAME = "brokerpro_service"
PASSWORD = "BrokerPro@Service2026"

TOKEN_FILE = os.path.join(
    os.path.dirname(__file__),
    "..",
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


def login():

    response = requests.post(

        f"{BASE_URL}/api/token/",

        json={
            "username": USERNAME,
            "password": PASSWORD
        }

    )
    print("STATUS:", response.status_code)
    print("BODY:", response.text)

    tokens = response.json()

    save_tokens(tokens)

    return tokens


def get_access_token():

    tokens = login()

    return tokens["access"]