from office365.sharepoint.publishing.pages.fields_data import SitePageFieldsData


class CampaignPublicationFieldsData(SitePageFieldsData):

    def __init__(
        self,
        endpoint_email: str = None,
        endpoint_share_point: str = None,
        endpoint_teams: str = None,
        endpoint_viva_engage: str = None,
        endpoint_yammer: str = None,
        publication_metadata: str = None,
        publication_status: int = None,
    ):
        super().__init__()
        self.EndpointEmail = endpoint_email
        self.EndpointSharePoint = endpoint_share_point
        self.EndpointTeams = endpoint_teams
        self.EndpointVivaEngage = endpoint_viva_engage
        self.EndpointYammer = endpoint_yammer
        self.PublicationMetadata = publication_metadata
        self.PublicationStatus = publication_status

    @property
    def entity_type_name(self):
        return "SP.Publishing.CampaignPublicationFieldsData"
