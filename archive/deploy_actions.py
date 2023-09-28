import requests
import time
import os
import json
import sys

ACTION = 'set-claims-as-github-teams'

# read access_token from ephemeral (generated by pipeline) file
with open('access_token', 'r') as file:
    auth_token = file.read().rstrip()

# setup endpoint parameters
header = {
  "Authorization": f"Bearer {auth_token}",
  'Accept': 'application/json'
}
url = f"https://{os.environ.get('TENANT')}.us.auth0.com/api/v2/actions/actions"

# deploy auth0.action
response = requests.get(url, headers=header)
for app in response.json()['actions']:
    if app['name'] == ACTION:
        print(f"{ACTION} exists: deploying...")
        try:
          deploy_result = requests.post(f"{url}/{app['id']}/deploy", headers=header, data={})
          deploy_result.raise_for_status()
        except requests.exceptions.HTTPError as err:
          print(f"deploy: {err.args[0]}")
