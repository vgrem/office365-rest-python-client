from typing import Optional
from uuid import UUID

from office365.sharepoint.entity import Entity


class OrgRelationVerification(Entity):
    @property
    def partner_site_subscription_id(self) -> Optional[UUID]:
        """Gets the PartnerSiteSubscriptionId property"""
        return self.properties.get("PartnerSiteSubscriptionId", None)

    @property
    def result(self) -> Optional[str]:
        """Gets the Result property"""
        return self.properties.get("Result", None)

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.MultiGeo.Service.OrgRelationVerification"
