from typing import List

from office365.directory.applications.implicitgrantsettings import ImplicitGrantSettings
from office365.directory.applications.redirecturisettings import RedirectUriSettings
from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.collections import StringCollection


class WebApplication(ClientValue):
    """Specifies settings for a web application."""

    def __init__(
        self,
        home_page_url: str = None,
        logout_url: str = None,
        redirect_uris: List[str] = None,
        implicit_grant_settings: ImplicitGrantSettings = ImplicitGrantSettings(),
        redirect_uri_settings: ClientValueCollection[RedirectUriSettings] = ClientValueCollection(RedirectUriSettings),
    ):
        """
        :param str home_page_url: Home page or landing page of the application.
        :param str logout_url: Specifies the URL that will be used by Microsoft's authorization service to logout an
            user using front-channel, back-channel or SAML logout protocols.
        :param list[str] redirect_uris: Specifies the URLs where user tokens are sent for sign-in, or the redirect
            URIs where OAuth 2.0 authorization codes and access tokens are sent.
        """
        self.homePageUrl = home_page_url
        self.logoutUrl = logout_url
        self.redirectUris = StringCollection(redirect_uris)
        self.implicitGrantSettings = implicit_grant_settings
        self.redirectUriSettings = redirect_uri_settings

    @property
    def entity_type_name(self):
        return "microsoft.graph.WebApplication"
