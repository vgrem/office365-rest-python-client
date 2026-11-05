from typing import Optional

from office365.runtime.client_value import ClientValue


class GetTeamChannelSiteOwnerResponse(ClientValue):
    Owner: Optional[str] = None
    SecondaryContact: Optional[str] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Portal.GetTeamChannelSiteOwnerResponse"
