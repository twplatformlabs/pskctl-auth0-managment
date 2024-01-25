
The resulting configuration supports an authentication flow meant to be used by a human. To QA either tenant:  

1. request device authorization code.  

```bash
curl --request POST \
  --url 'https://dev-pskctl.us.auth0.com/oauth/device/code' \
  --header 'content-type: application/x-www-form-urlencoded' \
  --data 'client_id=******567g35' \
  --data 'scope=openid offline_access' \
  --data 'audience=https://dev-pskctl.us.auth0.com/api/v2/'
```

2. Note the device_code and verification_uri_complete in the response.  

3. Use the verification_uri_complete link in  your browser to complete the device and user authentication. Will appear similar to:  
```
https://dev-pskctl.us.auth0.com/activate?user_code=XXXX-XXXX
```

4. Using the device_code, request an oidc token.
```
curl --request POST \
  --url 'https://dev-pskctl.us.auth0.com/oauth/token' \
  --header 'content-type: application/x-www-form-urlencoded' \
  --data grant_type=urn:ietf:params:oauth:grant-type:device_code \
  --data 'device_code=*****mnLg' \
  --data 'client_id=******567g35'
```
The token received will contain the following info:
```
{
    "access_token": "*****O8EDn9A",
    "refresh_token": "*****j8bYK",
    "id_token": "*****lhwgf==",
    "scope": "openid offline_access",
    "expires_in": 86400,
    "token_type": "Bearer"
}
```

5. Go to jwt.io and place the contents of the id_token into the `Encoded` box.  
The display should show the Signature as verfied and the contents of the id token will include the following:  
```
{
  "https://github.org/ThoughtWorks-DPS/teams": [
    "ThoughtWorks-DPS/demo",
    "ThoughtWorks-DPS/demo-publications",
    "ThoughtWorks-DPS/demo-reviews",
    "ThoughtWorks-DPS/twdps",
    "ThoughtWorks-DPS/twdps-core-collab-team",
    "ThoughtWorks-DPS/twdps-core-labs-team",
    "ThoughtWorks-DPS/twdps-orb-authors",
    "ThoughtWorks-DPS/twdps-sme"
  ],
  "cli": "dev-pskctl",
  "iss": "https://dev-pskctl.us.auth0.com/",
  ...
}
```
The list of teams will be all those teams in which  you are a member in the ThoughtWorks-DPS github org.
