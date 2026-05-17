from datetime import datetime
from typing import Optional
from uuid import UUID

from office365.sharepoint.entity import Entity


class SPAllOrgSGMetadata(Entity):
    @property
    def all_organization_security_group_id(self) -> Optional[UUID]:
        """Gets the AllOrganizationSecurityGroupId property"""
        return self.properties.get("AllOrganizationSecurityGroupId", None)

    @property
    def creation_time_in_utc(self) -> datetime:
        """Gets the CreationTimeInUtc property"""
        return self.properties.get("CreationTimeInUtc", datetime.min)

    @property
    def site_subscription_id(self) -> Optional[UUID]:
        """Gets the SiteSubscriptionId property"""
        return self.properties.get("SiteSubscriptionId", None)

    @property
    def status_code(self) -> Optional[int]:
        """Gets the StatusCode property"""
        return self.properties.get("StatusCode", None)

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.IdentityModel.SPAllOrgSGMetadata"
