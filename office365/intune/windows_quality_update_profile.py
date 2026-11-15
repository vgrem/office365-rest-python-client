from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from typing_extensions import Self

from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.intune.expedited_windows_quality_update_settings import ExpeditedWindowsQualityUpdateSettings
from office365.permissions import require_permission
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.runtime.types.collections import StringCollection
from office365.runtime.types.odata_property import odata, version

if TYPE_CHECKING:
    from office365.intune.windows_quality_update_profile_assignment import WindowsQualityUpdateProfileAssignment


@version("beta")
class WindowsQualityUpdateProfile(Entity):
    @odata(name="createdDateTime")
    @property
    def created_date_time(self) -> Optional[datetime]:
        """Gets the createdDateTime property"""
        return self.properties.get("createdDateTime", None)

    @odata(name="deployableContentDisplayName")
    @property
    def deployable_content_display_name(self) -> Optional[str]:
        """Gets the deployableContentDisplayName property"""
        return self.properties.get("deployableContentDisplayName", None)

    @odata(name="description")
    @property
    def description(self) -> Optional[str]:
        """Gets the description property"""
        return self.properties.get("description", None)

    @odata(name="displayName")
    @property
    def display_name(self) -> Optional[str]:
        """Gets the displayName property"""
        return self.properties.get("displayName", None)

    @odata(name="expeditedUpdateSettings")
    @property
    def expedited_update_settings(self) -> Optional[ExpeditedWindowsQualityUpdateSettings]:
        """Gets the expeditedUpdateSettings property"""
        return self.properties.get("expeditedUpdateSettings", None)

    @odata(name="lastModifiedDateTime")
    @property
    def last_modified_date_time(self) -> Optional[datetime]:
        """Gets the lastModifiedDateTime property"""
        return self.properties.get("lastModifiedDateTime", None)

    @odata(name="releaseDateDisplayName")
    @property
    def release_date_display_name(self) -> Optional[str]:
        """Gets the releaseDateDisplayName property"""
        return self.properties.get("releaseDateDisplayName", None)

    @odata(name="roleScopeTagIds")
    @property
    def role_scope_tag_ids(self) -> StringCollection:
        """Gets the roleScopeTagIds property"""
        return self.properties.get("roleScopeTagIds", StringCollection())

    @odata(name="assignments", navigation=True)
    @property
    def assignments(self) -> EntityCollection[WindowsQualityUpdateProfileAssignment]:
        """Gets the assignments property"""
        from office365.intune.windows_quality_update_profile_assignment import WindowsQualityUpdateProfileAssignment

        return self.properties.get(
            "assignments",
            EntityCollection[WindowsQualityUpdateProfileAssignment](
                self.context, WindowsQualityUpdateProfileAssignment, ResourcePath("assignments", self.resource_path)
            ),
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.WindowsQualityUpdateProfile"

    @require_permission(
        delegated=["DeviceManagementConfiguration.ReadWrite.All"],
        application=["DeviceManagementConfiguration.ReadWrite.All"],
    )
    def assign(self, assignments: ClientValueCollection[WindowsQualityUpdateProfileAssignment]) -> Self:
        """assign operation.

        Args:
            assignments (ClientValueCollection[WindowsQualityUpdateProfileAssignment]):
                assignments parameter
        """
        qry = ServiceOperationQuery(self, "assign", None, {"assignments": assignments}, None, None)
        self.context.add_query(qry)
        return self
