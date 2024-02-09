<div align="center">
	<p>
		<img alt="Thoughtworks Logo" src="https://raw.githubusercontent.com/ThoughtWorks-DPS/static/master/thoughtworks_flamingo_wave.png?sanitize=true" width=200 />
    <br />
		<img alt="DPS Title" src="https://raw.githubusercontent.com/ThoughtWorks-DPS/static/master/EMPCPlatformStarterKitsImage.png?sanitize=true" width=350/>
	</p>
  <br />
  <h3>pskctl-auth0-management</h3>
</div>
<br />

Configuration of Auth0 applications, social integrations, and actions to support the EMPC labs Platform Starter Kits engineering platform user experience.  

PSK Platform access is based around team membership. If you are part of a team that has been authorized to use the platform, then you will have permission to interact with all of that particular teams resources on the platform.  

The intended integration pattern is that all the SaaS developer tools are integrated into the organization's SSO provider. Generally, corporations have Okta (of which Auth0 is now a part) or another IDP (Azure AD) and this is used to create an authentication workflow with the tool. As the authorization experience is intended to be around team membership and we also want customers of the platform to be able to self-manage those teams, we will use GitHub as the oauth2 integration point for the platform. It is relatively straightforward to configure such an experience within GitHub itself (and most organization have) as far creating and managing teams in an authorized manner.  

A User (customer, developer) has access to the platform by virtue of being added to a GitHub Team that has been onboarded.  

The Auth0 tenant application created by this pipeline is used in two ways:  
- An the 0auth2/oidc integration with each of the kubernetes cluster to enable bounded access to team resources on the cluster, and
- to authN/Z calls to the custom platfom product APIs (typically using the platform cli `pskctl`).

The oauth0/oidc flow required by the pskctl tool is available in the free tier of Auth0. Complete these [bootstrap](doc/bootstrap.md) steps, using your own cli and tenant identies, as part of signing up for Auth0 and preparing for the pipeline managed Auth0 configuration.  

With a management api token now available, this pipeline will perform the following tasks:

* Create an application client to be used by the pskctl tool.

* Create a custom action that will run after a successful github social-authentication. The action fetches the Users teams for the integrated (above) github organization.  

* 'Deploy' the trigger integration so that the action runs immediately after authentication.

* Create the GitHub authentication integration and associate with the pskctl client application.

The above results in the creation of an oauth2/oidc device-auth-flow endpoint that will be used by the pskctl command line tool.

This endpoint implements the oauth2/oidc device-auth-flow. Using the pskctl cli, when you perform a `login` command, you will be provided a link. From your browser, proceed to the link and enter the provided device code. You must then authenticate to Github. This is performed via Githubs oauth service and no credential information is made available to Auth0.  

In addition to this social-login connection, upon a successful github login, the auth0 application client will fetch the list of organization github teams in which the user is a member. This list is included as a claim within the resulting id token.

The Auth0 tenant application is also integrated with the kubernetes clusters of the PSK engineering platform. The pskctl cli can also generate kubeconfig files that enable users to authenticate to the EKS cluster with permissions based on role bindings tied to the github team claims.  

### development

The above github oauth app and auth0 management api tokens must be available in th environment for the python scripts to work. See op.*.env  

These setting are all configurable in the request-body/TENANT.json file.
- token expires after 1hr (3600)
- can be refreshed (refresh token provided)
- absolute lifetime for refresh for token in active use is 7 days (604800)
- an idle token cannot be refreshed after 2days (172800)

[Maintainers notes](doc/maintainers.md)
