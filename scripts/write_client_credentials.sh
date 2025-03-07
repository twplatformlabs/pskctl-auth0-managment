#!/usr/bin/env bash
set -eo pipefail

export client=$1

if [[ -f "$client-client_credentials.json" ]]; then
  echo "write auth0 $client client credentials"
  Auth0ClientCredentials=$(jq . < $client-client_credentials.json)
  TenantClientID=$(echo $Auth0ClientCredentials | jq .client_id | sed 's/"//g' | tr -d \\n)
  TenantClientSecret=$(echo $Auth0ClientCredentials | jq .client_secret | sed 's/"//g' | tr -d \\n)

  op item edit 'svc-auth0' $client-cli-client-id=$TenantClientID --vault platform >/dev/null
  op item edit 'svc-auth0' $client-cli-client-secret=$TenantClientSecret --vault platform >/dev/null
else
  echo "Existing client updates. No new credentials generated."
fi
