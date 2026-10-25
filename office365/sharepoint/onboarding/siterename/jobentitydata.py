from typing import Optional
from uuid import UUID

from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity


class SiteRenameJobEntityData(Entity):
    @odata(name="OperationId")
    @property
    def operation_id(self) -> Optional[UUID]:
        """Gets the OperationId property"""
        return self.properties.get("OperationId", None)

    @odata(name="SkipGestures")
    @property
    def skip_gestures(self) -> Optional[str]:
        """Gets the SkipGestures property"""
        return self.properties.get("SkipGestures", None)

    @odata(name="SourceSiteUrl")
    @property
    def source_site_url(self) -> Optional[str]:
        """Gets the SourceSiteUrl property"""
        return self.properties.get("SourceSiteUrl", None)

    @odata(name="TargetSiteTitle")
    @property
    def target_site_title(self) -> Optional[str]:
        """Gets the TargetSiteTitle property"""
        return self.properties.get("TargetSiteTitle", None)

    @odata(name="TargetSiteUrl")
    @property
    def target_site_url(self) -> Optional[str]:
        """Gets the TargetSiteUrl property"""
        return self.properties.get("TargetSiteUrl", None)

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.Onboarding.RestService.Service.SiteRenameJobEntityData"
