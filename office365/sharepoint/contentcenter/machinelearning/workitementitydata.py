from __future__ import annotations

from typing import Optional
from uuid import UUID

from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity


class SPMachineLearningWorkItemEntityData(Entity):
    @odata(name="ExtraPropertyList")
    @property
    def extra_property_list(self) -> Optional[str]:
        """Gets the ExtraPropertyList property"""
        return self.properties.get("ExtraPropertyList", None)

    @odata(name="IsFolder")
    @property
    def is_folder(self) -> Optional[bool]:
        """Gets the IsFolder property"""
        return self.properties.get("IsFolder", None)

    @odata(name="ParentJobId")
    @property
    def parent_job_id(self) -> Optional[UUID]:
        """Gets the ParentJobId property"""
        return self.properties.get("ParentJobId", None)

    @odata(name="ProfileName")
    @property
    def profile_name(self) -> Optional[str]:
        """Gets the ProfileName property"""
        return self.properties.get("ProfileName", None)

    @odata(name="TargetServerRelativeUrl")
    @property
    def target_server_relative_url(self) -> Optional[str]:
        """Gets the TargetServerRelativeUrl property"""
        return self.properties.get("TargetServerRelativeUrl", None)

    @odata(name="TargetSiteId")
    @property
    def target_site_id(self) -> Optional[UUID]:
        """Gets the TargetSiteId property"""
        return self.properties.get("TargetSiteId", None)

    @odata(name="TargetSiteUrl")
    @property
    def target_site_url(self) -> Optional[str]:
        """Gets the TargetSiteUrl property"""
        return self.properties.get("TargetSiteUrl", None)

    @odata(name="TargetUniqueId")
    @property
    def target_unique_id(self) -> Optional[UUID]:
        """Gets the TargetUniqueId property"""
        return self.properties.get("TargetUniqueId", None)

    @odata(name="TargetWebId")
    @property
    def target_web_id(self) -> Optional[UUID]:
        """Gets the TargetWebId property"""
        return self.properties.get("TargetWebId", None)

    @odata(name="TargetWebServerRelativeUrl")
    @property
    def target_web_server_relative_url(self) -> Optional[str]:
        """Gets the TargetWebServerRelativeUrl property"""
        return self.properties.get("TargetWebServerRelativeUrl", None)

    @odata(name="Type")
    @property
    def type_(self) -> Optional[UUID]:
        """Gets the Type property"""
        return self.properties.get("Type", None)

    @property
    def entity_type_name(self):
        return "Microsoft.Office.Server.ContentCenter.SPMachineLearningWorkItemEntityData"

    @odata(name="Type")
    @property
    def type(self) -> Optional[UUID]:
        """Gets the Type property"""
        return self.properties.get("Type", None)
