<div align="center">
	<p>
		<img alt="Thoughtworks Logo" src="https://raw.githubusercontent.com/ThoughtWorks-DPS/static/master/thoughtworks_flamingo_wave.png?sanitize=true" width=200 />
    <br />
		<img alt="DPS Title" src="https://raw.githubusercontent.com/ThoughtWorks-DPS/static/master/EMPCPlatformStarterKitsImage.png?sanitize=true" width=350/>
	</p>
  <br />
  <h3>pskctl-auth0-management</h3>
    <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/github/license/ThoughtWorks-DPS/psk-aws-platform-vpc"></a> <a href="https://github.com"><img src="https://img.shields.io/badge/-social-blank.svg?style=social&logo=github"></a>
</div>
<br />

Configuration of Auth0 applications, social integrations, and actions to support the EMPC labs Platform Starter Kits command line tool (`pskctl`).  

The oauth0/oidc flow required by the pskctl tool is available in the free tier of Auth0. Complete these [bootstrap](doc/bootstrap.md) steps as part of signing up for Auth0 and preparing for the pipeline managed Auth0 configuration.  

With a management api token now available, this pipeline will perform the following tasks:

* Create an application client to be used by the pskctl tool. 

* Create a custom action that will run after a successful github social-authentication. The action fetches the Users teams for the integrated (above) github organization.  

* 'Deploy' the trigger integration so that the action runs immediately after authentication.

* Create the GitHub authentication integration and associate with the pskctl client application.

The above results in the creation of an oauth2/oidc device-auth-flow endpoint that will be used by the pskctl command line tool.

This endpoint implements the oauth2/oidc device-auth-flow. Using the pskctl cli, when you perform a `login` command, you will be provided a link. From your browser, proceed to the link and enter the provided device code. You must then authenticate to Github. This is performed via Githubs oauth service and no credential information is made available to Auth0.  

In addition to this social-login connection, upon a successful github login, the auth0 application client will fetch the list of github teams the user is a member of the github organization. This list is included as a claim within the resulting id token. 


### development

The above github oauth app and auth0 management api tokens must be available in th environment for the python scripts to work. See op.*.env  





- token expires after 1hr (3600)
- can be refreshed (refresh token provided)
- absolute lifetime for refresh for token in active use is 7 days (604800)
- an idle token cannot be refreshed after 2days (172800)







After completing the bootstrap steps, the github social connection in place and the Management API client endpoint available, now this repo pipeline can manage the Applications and Rules that define the functionality of our oidc endpoint.  

The pipeline has three essential steps:

1. Fetch a management api token to use for creating and updating Auth0 configuration
2. Deploy the dev or prod tenant dpsctl application definitions
3. Deploy all rules used by the dpsctl application login process

Since Auth0 is not used to perform any authentication functions, the rules are the steps to take in constructing a jwt to return from a successful authentication.  

In this case that means, if the user is a member of the github org where the github oauth-app is defined (in this case ThoughtWorks-DPS) then they will be able to successfully authenticate, after which:  

* with the users own github access token, fetch all org teams of which the user is a member
* insert those teams as a list into the returned idToken

See repo pipeline for specific details.  




