from typing import Optional
from uuid import UUID

from office365.sharepoint.entity import Entity


class SharePointSiteSharingInsights(Entity):

    @property
    def anyone(self) -> Optional[int]:
        """Gets the Anyone property"""
        return self.properties.get("Anyone", None)

    @property
    def end_date(self) -> Optional[str]:
        """Gets the EndDate property"""
        return self.properties.get("EndDate", None)

    @property
    def external(self) -> Optional[int]:
        """Gets the External property"""
        return self.properties.get("External", None)

    @property
    def internal(self) -> Optional[int]:
        """Gets the Internal property"""
        return self.properties.get("Internal", None)

    @property
    def is_missing(self) -> Optional[bool]:
        """Gets the IsMissing property"""
        return self.properties.get("IsMissing", None)

    @property
    def is_teams_connected(self) -> Optional[bool]:
        """Gets the IsTeamsConnected property"""
        return self.properties.get("IsTeamsConnected", None)

    @property
    def tenant_id(self) -> Optional[UUID]:
        """Gets the TenantId property"""
        return self.properties.get("TenantId", None)

    @property
    def schema_version(self) -> Optional[int]:
        """Gets the SchemaVersion property"""
        return self.properties.get("SchemaVersion", None)

    @property
    def security_group(self) -> Optional[int]:
        """Gets the SecurityGroup property"""
        return self.properties.get("SecurityGroup", None)

    @property
    def sensitivity_label(self) -> Optional[str]:
        """Gets the SensitivityLabel property"""
        return self.properties.get("SensitivityLabel", None)

    @property
    def share_point_group(self) -> Optional[int]:
        """Gets the SharePointGroup property"""
        return self.properties.get("SharePointGroup", None)

    @property
    def site_id(self) -> Optional[UUID]:
        """Gets the SiteId property"""
        return self.properties.get("SiteId", None)

    @property
    def site_name(self) -> Optional[str]:
        """Gets the SiteName property"""
        return self.properties.get("SiteName", None)

    @property
    def site_owner(self) -> Optional[str]:
        """Gets the SiteOwner property"""
        return self.properties.get("SiteOwner", None)

    @property
    def site_template_id(self) -> Optional[int]:
        """Gets the SiteTemplateId property"""
        return self.properties.get("SiteTemplateId", None)

    @property
    def site_url(self) -> Optional[str]:
        """Gets the SiteUrl property"""
        return self.properties.get("SiteUrl", None)

    @property
    def start_date(self) -> Optional[str]:
        """Gets the StartDate property"""
        return self.properties.get("StartDate", None)

    @property
    def total(self) -> Optional[int]:
        """Gets the Total property"""
        return self.properties.get("Total", None)

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.TenantAdministration.SharePointSiteSharingInsights"
