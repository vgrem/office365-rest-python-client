from typing import Optional

from office365.sharepoint.publishing.pages.fields_data import SitePageFieldsData


class CampaignPublicationFieldsData(SitePageFieldsData):
    def __init__(
        self,
        endpoint_email: Optional[str] = None,
        endpoint_share_point: Optional[str] = None,
        endpoint_teams: Optional[str] = None,
        endpoint_viva_engage: Optional[str] = None,
        endpoint_yammer: Optional[str] = None,
        publication_metadata: Optional[str] = None,
        publication_status: Optional[int] = None,
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
    def entity_type_name(self):  # type: ignore[override]
        return "SP.Publishing.CampaignPublicationFieldsData"
