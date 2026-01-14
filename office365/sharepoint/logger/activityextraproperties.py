from office365.runtime.client_value import ClientValue


class LogActivityExtraProperties(ClientValue):
    def __init__(
        self,
        campaign_metadata: str = None,
        is_web_welcome_page: bool = None,
        link_url_clicked: str = None,
    ):
        self.CampaignMetadata = campaign_metadata
        self.IsWebWelcomePage = is_web_welcome_page
        self.LinkUrlClicked = link_url_clicked

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Internal.LogActivityExtraProperties"
