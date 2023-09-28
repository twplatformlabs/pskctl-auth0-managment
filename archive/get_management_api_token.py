import os
import json
import requests

def get_access_token(tenant, client_id, client_secret):
    url = f"https://{os.environ.get('TENANT')}.us.auth0.com/oauth/token"
    payload = {
        'client_id': tenant,
        'client_secret': client_id,
        'audience': client_secret,
        'grant_type': 'client_credentials'
    }

    headers = {'content-type': 'application/json'}

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        data = response.json()
        access_token = data.get('access_token')
        return access_token
    else:
        print("Error obtaining access token:")
        print(response.status_code, response.text)
        return None
