import http.client
import json
import os

conn = http.client.HTTPSConnection(f"{os.environ.get('TENANT')}.us.auth0.com")
payload = f"{{\"client_id\":\"{os.environ.get('MANAGEMENT_API_CLIENT_ID')}\",\"client_secret\":\"{os.environ.get('MANAGEMENT_API_CLIENT_SECRET')}\",\"audience\":\"https://{os.environ.get('TENANT')}.us.auth0.com/api/v2/\",\"grant_type\":\"client_credentials\"}}"

headers = { 'content-type': "application/json" }

conn.request("POST", "/oauth/token", payload, headers)

res = conn.getresponse()
data = json.loads(res.read().decode("utf-8"))

text_file = open("access_token", "w")
err = text_file.write(data['access_token'])
text_file.close()
