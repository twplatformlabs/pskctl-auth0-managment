/**
* Handler that will be called during the execution of a PostLogin flow.
*
* @param {Event} event - Details about the user and the context in which they are logging in.
* @param {PostLoginAPI} api - Interface whose methods can be used to change the behavior of the login.
*/
exports.onExecutePostLogin = async (event, api) => {

  const requiredOrganization = 'YOUR_REQUIRED_ORGANIZATION'; // Replace with your GitHub organization name

  // get users social_connection access token
  const { ManagementClient } = require('auth0');
  const management = new ManagementClient({
    domain: 'dev-pskctl.us.auth0.com',
    clientId: event.secrets.MANAGEMENT_API_CLIENT_ID,
    clientSecret: event.secrets.MANAGEMENT_API_CLIENT_SECRET,
    scope: 'read:users'
  });
  const social_metadata = await management.getUser({ id: event.user.user_id });
  var github = social_metadata.identities.filter(function (id){
                 return id.provider === 'github';
               })[0];
  var access_token = github.access_token;

  // fetch the user's GitHub team memberships
  const axios = require("axios");
  const githubAPIUrl = 'https://api.github.com/user/teams';
  const options = {
    headers: {
      'Authorization': `token ${access_token}`,
      'User-Agent': 'dev-pskctl'
    }
  };

  try {
    var response = await axios.get(githubAPIUrl, options);
    var github_teams = response.data.map(function(team) {
      return team.organization.login + "/" + team.slug;
    });

    // Check if the user is part of the required organization
    const isInOrganization = response.data.some(team => team.organization.login === requiredOrganization);

    if (!isInOrganization) {
      // User is not part of the required organization, return an error
      if (event.authorization) {
        api.idToken.setCustomClaim("github_teams_error", `User is not a member of the required GitHub organization: ${requiredOrganization}`);
      }
        return api.accessDenied(`User is not a member of the required GitHub organization: ${requiredOrganization}`);

    }

    // add teams list as claims to jwt
    if (event.authorization) {
      api.idToken.setCustomClaim("https://github.org/twplatformlabs/teams", github_teams);
      api.idToken.setCustomClaim("cli", "dev-pskctl");
    }

  } catch (error) {
    // add the error message to the custom claims
    console.error('Error fetching GitHub team memberships:', error.message);
    if (event.authorization) {
      api.idToken.setCustomClaim("github_teams_error", error.message);
    }
    return api.accessDenied("Error fetching github teams: "+ error.message)
  }

};