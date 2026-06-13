from __future__ import annotations

from office365.sharepoint.publishing.pages.fields_data import SitePageFieldsData


class CampaignPublicationFieldsData(SitePageFieldsData):
    EndpointEmail: str | None = None
    EndpointSharePoint: str | None = None
    EndpointTeams: str | None = None
    EndpointVivaEngage: str | None = None
    EndpointYammer: str | None = None
    PublicationStatus: int | None = None

    @property
    def entity_type_name(self):
        return "SP.Publishing.CampaignPublicationFieldsData"
