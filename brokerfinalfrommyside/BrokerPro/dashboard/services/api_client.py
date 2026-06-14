import requests

from .token_manager import get_access_token

BASE_URL = "http://127.0.0.1:8000"

def get_dashboard_property(id, username):

    response = get(

        f"/api/dashboard/properties/preview/{id}/",

        username

    )

    return response.json()
def get_preview_properties(username):

    response = get(
        "/api/dashboard/properties/preview/",
        username
    )

    return response.json()

def get_dashboard_properties(username):

    response = get(

        "/api/dashboard/properties/",

        username

    )

    return response.json()

def get(endpoint, username):

    token = get_access_token(username)

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(
        f"{BASE_URL}{endpoint}",
        headers=headers
    )

    return response


def post(endpoint, username, data=None, files=None):

    token = get_access_token(username)

    headers = {
        "Authorization": f"Bearer {token}"
    }

    upload_files = None

    if files:

        # Already converted list
        if isinstance(files, list):

            upload_files = files

        # Django MultiValueDict
        elif hasattr(files, "getlist"):

            upload_files = []

            for key in files:

                for file in files.getlist(key):

                    upload_files.append(
                        (
                            key,
                            (
                                file.name,
                                file,
                                file.content_type
                            )
                        )
                    )

    response = requests.post(
        f"{BASE_URL}{endpoint}",
        data=data,
        files=upload_files,
        headers=headers
    )

    return response

def put(endpoint, username, data=None, files=None):

    token = get_access_token(username)

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.put(
        f"{BASE_URL}{endpoint}",
        data=data,
        files=files,
        headers=headers
    )

    return response

def delete(endpoint, username):

    token = get_access_token(username)

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.delete(
        f"{BASE_URL}{endpoint}",
        headers=headers
    )

    return response

