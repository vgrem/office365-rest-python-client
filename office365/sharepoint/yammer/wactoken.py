from office365.runtime.client_value import ClientValue


class WacToken(ClientValue):

    def __init__(
        self,
        access_token: str = None,
        access_token_ttl: int = None,
        app_url: str = None,
        error_message_to_display: str = None,
        fav_icon_target: str = None,
        redirect_url: str = None,
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
