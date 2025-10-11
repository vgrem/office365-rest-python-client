from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


class SPACSServicePrincipalInfo(ClientValue):

    def __init__(
        self,
        application_endpoint_authorities=None,
        display_name=None,
        app_domains: StringCollection = None,
        app_id: str = None,
        app_identifier: str = None,
        redirect_uri: str = None,
        title: str = None,
    ):
        self.ApplicationEndpointAuthorities = StringCollection(application_endpoint_authorities)
        self.DisplayName = display_name
        self.appDomains = app_domains
        self.appId = app_id
        self.appIdentifier = app_identifier
        self.redirectUri = redirect_uri
        self.title = title

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Authentication.SPACSServicePrincipalInfo"
