from typing import Optional

from office365.runtime.client_value import ClientValue


class WacToken(ClientValue):
    def __init__(
        self,
        access_token: Optional[str] = None,
        access_token_ttl: Optional[int] = None,
        app_url: Optional[str] = None,
        error_message_to_display: Optional[str] = None,
        fav_icon_target: Optional[str] = None,
        redirect_url: Optional[str] = None,
    ):
        self.AccessToken = access_token
        self.AccessTokenTtl = access_token_ttl
        self.AppUrl = app_url
        self.ErrorMessageToDisplay = error_message_to_display
        self.FavIconTarget = fav_icon_target
        self.RedirectUrl = redirect_url

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Yammer.WacToken"
