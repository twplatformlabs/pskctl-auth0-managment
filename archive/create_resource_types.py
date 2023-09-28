import requests
import time
import json
from format_api_json_payloads import format_action_payload
from auth0.management import Auth0
from auth0.exceptions import Auth0Error

from config import tenant

def ca(auth0, custom_action):
    """create or patch action"""

    with open('request-body/create-action-body.json', 'r') as file:
        body = json.load(file)
    response = auth0.actions.get_actions()

    # patch action if it already exists
    for act in response['actions']:
        if act['name'] == custom_action:
          print(f"{custom_action} exists: patching...")
          try:
            next_response = auth0.actions.update_action(act['id'], body)
          except Auth0Error as err:
              print(err)


def create_action(tenant, auth_token, action):
    format_action_payload()

    # setup endpoint parameters
    header = {
      "Authorization": f"Bearer {auth_token}",
      'Accept': 'application/json'
    }
    url = f"https://{tenant}.us.auth0.com/api/v2/actions/actions"
    with open('request-body/create-action-body.json', 'r') as file:
        body = json.load(file)

    # create or patch auth0.action
    patched = False
    response = requests.get(url, headers=header)
    for app in response.json()['actions']:
        if app['name'] == action:
            print(f"{action} exists: patching...")
            try:
              patch_result = requests.patch(f"{url}/{app['id']}", headers=header, json=body)
              patch_result.raise_for_status()

              # if you call deploy very quickly after a patch it fails with 400
              time.sleep(10)

              deploy_result = requests.post(f"{url}/{app['id']}/deploy", headers=header, data={})
              deploy_result.raise_for_status()
              applied = False
            except requests.exceptions.HTTPError as err:
              print({err.args[0]})

    if not patched:
        print(f"creating {action}...")
        try:
          post_result = requests.post(url, headers=header, json=body)
          post_result.raise_for_status()

          # if you call deploy very quickly after a patch it fails with 400
          time.sleep(10)

          deploy_result = requests.post(f"{url}/{post_result.json['id']}/deploy", headers=header, data={})
          deploy_result.raise_for_status()
        except requests.exceptions.HTTPError as err:
          print({err.args[0]})

    # need the newly create/patched/deployed action json body to create trigger binding
    response = requests.get(url, headers=header)
    for app in response.json()['actions']:
        if app['name'] == action:
            print(f"{action} exists: patching...")
            try:
              patch_result = requests.patch(f"{url}/{app['id']}", headers=header, json=body)
              patch_result.raise_for_status()

              # if you call deploy very quickly after a patch it fails with 400
              time.sleep(10)

              deploy_result = requests.post(f"{url}/{app['id']}/deploy", headers=header, data={})
              deploy_result.raise_for_status()
              applied = False
            except requests.exceptions.HTTPError as err:
              print({err.args[0]})
