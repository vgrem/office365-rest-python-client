from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from typing_extensions import Self

from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.intune.windows_update_rollout_settings import WindowsUpdateRolloutSettings
from office365.permissions import require_permission
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.runtime.types.collections import StringCollection
from office365.runtime.types.odata_property import odata, version

if TYPE_CHECKING:
    from office365.intune.windows_feature_update_profile_assignment import WindowsFeatureUpdateProfileAssignment


@version("beta")
class WindowsFeatureUpdateProfile(Entity):
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

    @odata(name="endOfSupportDate")
    @property
    def end_of_support_date(self) -> Optional[datetime]:
        """Gets the endOfSupportDate property"""
        return self.properties.get("endOfSupportDate", None)

    @odata(name="featureUpdateVersion")
    @property
    def feature_update_version(self) -> Optional[str]:
        """Gets the featureUpdateVersion property"""
        return self.properties.get("featureUpdateVersion", None)

    @odata(name="installFeatureUpdatesOptional")
    @property
    def install_feature_updates_optional(self) -> Optional[bool]:
        """Gets the installFeatureUpdatesOptional property"""
        return self.properties.get("installFeatureUpdatesOptional", None)

    @odata(name="installLatestWindows10OnWindows11IneligibleDevice")
    @property
    def install_latest_windows10_on_windows11_ineligible_device(self) -> Optional[bool]:
        """Gets the installLatestWindows10OnWindows11IneligibleDevice property"""
        return self.properties.get("installLatestWindows10OnWindows11IneligibleDevice", None)

    @odata(name="lastModifiedDateTime")
    @property
    def last_modified_date_time(self) -> Optional[datetime]:
        """Gets the lastModifiedDateTime property"""
        return self.properties.get("lastModifiedDateTime", None)

    @odata(name="roleScopeTagIds")
    @property
    def role_scope_tag_ids(self) -> StringCollection:
        """Gets the roleScopeTagIds property"""
        return self.properties.get("roleScopeTagIds", StringCollection())

    @odata(name="rolloutSettings")
    @property
    def rollout_settings(self) -> Optional[WindowsUpdateRolloutSettings]:
        """Gets the rolloutSettings property"""
        return self.properties.get("rolloutSettings", None)

    @odata(name="assignments", navigation=True)
    @property
    def assignments(self) -> EntityCollection[WindowsFeatureUpdateProfileAssignment]:
        """Gets the assignments property"""
        from office365.intune.windows_feature_update_profile_assignment import WindowsFeatureUpdateProfileAssignment

        return self.properties.get(
            "assignments",
            EntityCollection[WindowsFeatureUpdateProfileAssignment](
                self.context, WindowsFeatureUpdateProfileAssignment, ResourcePath("assignments", self.resource_path)
            ),
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.WindowsFeatureUpdateProfile"

    @require_permission(
        delegated=["DeviceManagementConfiguration.ReadWrite.All"],
        application=["DeviceManagementConfiguration.ReadWrite.All"],
    )
    def assign(self, assignments: ClientValueCollection[WindowsFeatureUpdateProfileAssignment]) -> Self:
        """assign operation.

        Args:
            assignments (ClientValueCollection[WindowsFeatureUpdateProfileAssignment]):
                assignments parameter
        """
        qry = ServiceOperationQuery(self, "assign", None, {"assignments": assignments}, None, None)
        self.context.add_query(qry)
        return self
