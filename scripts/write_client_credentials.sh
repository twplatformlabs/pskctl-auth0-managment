#!/usr/bin/env bash

set -e

echo "write auth0 application client credentials"
Auth0ClientCredentials=$(cat client_credentials.json | jq .)

op item edit 'svc-auth0' $TENANT-cli-client-id=$(echo $Auth0ClientCredentials | jq .client_id | sed 's/"//g' | tr -d \\n) >/dev/null
op item edit 'svc-auth0' $TENANT-cli-client-secret=$(echo $Auth0ClientCredentials | jq .client_secret | sed 's/"//g' | tr -d \\n) >/dev/null
