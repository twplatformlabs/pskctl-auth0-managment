#!/usr/bin/env bash
set -eo pipefail

if [[ -f "client_credentials.json" ]]; then
  echo "write auth0 application client credentials"
  Auth0ClientCredentials=$(jq . < client_credentials.json)
  TenantClientID=$(echo $Auth0ClientCredentials | jq .client_id | sed 's/"//g' | tr -d \\n)
  TenantClientSecret=$(echo $Auth0ClientCredentials | jq .client_secret | sed 's/"//g' | tr -d \\n)

  op item edit 'svc-auth0' $TENANT-cli-client-id=$TenantClientID --vault empc-lab >/dev/null
  op item edit 'svc-auth0' $TENANT-cli-client-secret=$TenantClientSecret --vault empc-lab >/dev/null
else
  echo "Existing client updates. No new credentials generated."
fi
