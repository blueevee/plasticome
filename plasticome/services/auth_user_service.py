import os

import requests
from dotenv import load_dotenv

load_dotenv(override=True)


def authenticate_user(username: str, secret: str):

    auth_data = {'username': username, 'secret': secret}

    response = requests.post(
        f"{os.getenv('PLASTICOME_METADATA_URL')}/auth", json=auth_data
    )

    if response.status_code == 200:
        data = response.json()
        token = data.get('access_token')
        return token, False
    return False, True
