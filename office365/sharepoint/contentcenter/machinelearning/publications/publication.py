from __future__ import annotations

from datetime import datetime
from typing import Optional
from uuid import UUID

from typing_extensions import Self

from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity


class SPMachineLearningPublication(Entity):
    @property
    def entity_type_name(self):
        return "Microsoft.Office.Server.ContentCenter.SPMachineLearningPublication"

    @odata(name="Created")
    @property
    def created(self) -> Optional[datetime]:
        """Gets the Created property"""
        return self.properties.get("Created", datetime.min)

    @odata(name="CreatedBy")
    @property
    def created_by(self) -> Optional[str]:
        """Gets the CreatedBy property"""
        return self.properties.get("CreatedBy", None)

    @odata(name="DriveId")
    @property
    def drive_id(self) -> Optional[str]:
        """Gets the DriveId property"""
        return self.properties.get("DriveId", None)

    @odata(name="HasTargetSitePermission")
    @property
    def has_target_site_permission(self) -> Optional[bool]:
        """Gets the HasTargetSitePermission property"""
        return self.properties.get("HasTargetSitePermission", None)

    @odata(name="ID")
    @property
    def id_(self) -> Optional[int]:
        """Gets the ID property"""
        return self.properties.get("ID", None)

    @odata(name="ModelId")
    @property
    def model_id(self) -> Optional[int]:
        """Gets the ModelId property"""
        return self.properties.get("ModelId", None)

    @odata(name="ModelName")
    @property
    def model_name(self) -> Optional[str]:
        """Gets the ModelName property"""
        return self.properties.get("ModelName", None)

    @odata(name="ModelType")
    @property
    def model_type(self) -> Optional[int]:
        """Gets the ModelType property"""
        return self.properties.get("ModelType", None)

    @odata(name="ModelUniqueId")
    @property
    def model_unique_id(self) -> Optional[UUID]:
        """Gets the ModelUniqueId property"""
        return self.properties.get("ModelUniqueId", None)

    @odata(name="ModelVersion")
    @property
    def model_version(self) -> Optional[str]:
        """Gets the ModelVersion property"""
        return self.properties.get("ModelVersion", None)

    @odata(name="Modified")
    @property
    def modified(self) -> Optional[datetime]:
        """Gets the Modified property"""
        return self.properties.get("Modified", datetime.min)

    @odata(name="ModifiedBy")
    @property
    def modified_by(self) -> Optional[str]:
        """Gets the ModifiedBy property"""
        return self.properties.get("ModifiedBy", None)

    @odata(name="ObjectId")
    @property
    def object_id(self) -> Optional[str]:
        """Gets the ObjectId property"""
        return self.properties.get("ObjectId", None)

    @odata(name="PublicationType")
    @property
    def publication_type(self) -> Optional[int]:
        """Gets the PublicationType property"""
        return self.properties.get("PublicationType", None)

    @odata(name="TargetLibraryId")
    @property
    def target_library_id(self) -> Optional[UUID]:
        """Gets the TargetLibraryId property"""
        return self.properties.get("TargetLibraryId", None)

    @odata(name="TargetLibraryName")
    @property
    def target_library_name(self) -> Optional[str]:
        """Gets the TargetLibraryName property"""
        return self.properties.get("TargetLibraryName", None)

    @odata(name="TargetLibraryRemoved")
    @property
    def target_library_removed(self) -> Optional[bool]:
        """Gets the TargetLibraryRemoved property"""
        return self.properties.get("TargetLibraryRemoved", None)

    @odata(name="TargetLibraryServerRelativeUrl")
    @property
    def target_library_server_relative_url(self) -> Optional[str]:
        """Gets the TargetLibraryServerRelativeUrl property"""
        return self.properties.get("TargetLibraryServerRelativeUrl", None)

    @odata(name="TargetLibraryUrl")
    @property
    def target_library_url(self) -> Optional[str]:
        """Gets the TargetLibraryUrl property"""
        return self.properties.get("TargetLibraryUrl", None)

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

    @odata(name="TargetTableListId")
    @property
    def target_table_list_id(self) -> Optional[UUID]:
        """Gets the TargetTableListId property"""
        return self.properties.get("TargetTableListId", None)

    @odata(name="TargetTableListName")
    @property
    def target_table_list_name(self) -> Optional[str]:
        """Gets the TargetTableListName property"""
        return self.properties.get("TargetTableListName", None)

    @odata(name="TargetTableListRemoved")
    @property
    def target_table_list_removed(self) -> Optional[bool]:
        """Gets the TargetTableListRemoved property"""
        return self.properties.get("TargetTableListRemoved", None)

    @odata(name="TargetTableListServerRelativeUrl")
    @property
    def target_table_list_server_relative_url(self) -> Optional[str]:
        """Gets the TargetTableListServerRelativeUrl property"""
        return self.properties.get("TargetTableListServerRelativeUrl", None)

    @odata(name="TargetTableListUrl")
    @property
    def target_table_list_url(self) -> Optional[str]:
        """Gets the TargetTableListUrl property"""
        return self.properties.get("TargetTableListUrl", None)

    @odata(name="TargetWebId")
    @property
    def target_web_id(self) -> Optional[UUID]:
        """Gets the TargetWebId property"""
        return self.properties.get("TargetWebId", None)

    @odata(name="TargetWebName")
    @property
    def target_web_name(self) -> Optional[str]:
        """Gets the TargetWebName property"""
        return self.properties.get("TargetWebName", None)

    @odata(name="TargetWebServerRelativeUrl")
    @property
    def target_web_server_relative_url(self) -> Optional[str]:
        """Gets the TargetWebServerRelativeUrl property"""
        return self.properties.get("TargetWebServerRelativeUrl", None)

    @odata(name="UniqueId")
    @property
    def unique_id(self) -> Optional[UUID]:
        """Gets the UniqueId property"""
        return self.properties.get("UniqueId", None)

    @odata(name="ViewOption")
    @property
    def view_option(self) -> Optional[str]:
        """Gets the ViewOption property"""
        return self.properties.get("ViewOption", None)

    def delete(self) -> Self:
        """Delete operation."""
        qry = ServiceOperationQuery(self, "Delete")
        self.context.add_query(qry)
        return self

    @odata(name="ID")
    @property
    def id(self) -> Optional[int]:
        """Gets the ID property"""
        return self.properties.get("ID", None)
