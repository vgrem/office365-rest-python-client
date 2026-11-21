from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from typing_extensions import Self

from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.permissions import require_permission, requires_license
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.runtime.types.collections import StringCollection
from office365.runtime.types.odata_property import odata, version

if TYPE_CHECKING:
    from office365.intune.devices.management.windows_defender_application_control_supplemental_policy_assignment import (
        WindowsDefenderApplicationControlSupplementalPolicyAssignment,
    )
    from office365.intune.devices.management.windows_defender_application_control_supplemental_policy_deployment_status import (  # noqa: E501
        WindowsDefenderApplicationControlSupplementalPolicyDeploymentStatus,
    )
    from office365.intune.devices.management.windows_defender_application_control_supplemental_policy_deployment_summary import (  # noqa: E501
        WindowsDefenderApplicationControlSupplementalPolicyDeploymentSummary,
    )


@version("beta")
@requires_license("INTUNE_A")
class WindowsDefenderApplicationControlSupplementalPolicy(Entity):
    @odata(name="content")
    @property
    def content(self) -> Optional[bytes]:
        """Gets the content property"""
        return self.properties.get("content", None)

    @odata(name="contentFileName")
    @property
    def content_file_name(self) -> Optional[str]:
        """Gets the contentFileName property"""
        return self.properties.get("contentFileName", None)

    @odata(name="creationDateTime")
    @property
    def creation_date_time(self) -> Optional[datetime]:
        """Gets the creationDateTime property"""
        return self.properties.get("creationDateTime", None)

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

    @odata(name="version")
    @property
    def version(self) -> Optional[str]:
        """Gets the version property"""
        return self.properties.get("version", None)

    @odata(name="assignments", navigation=True)
    @property
    def assignments(self) -> EntityCollection[WindowsDefenderApplicationControlSupplementalPolicyAssignment]:
        """Gets the assignments property"""
        from office365.intune.devices.management.windows_defender_application_control_supplemental_policy_assignment import (  # noqa: E501
            WindowsDefenderApplicationControlSupplementalPolicyAssignment,
        )

        return self.properties.get(
            "assignments",
            EntityCollection[WindowsDefenderApplicationControlSupplementalPolicyAssignment](
                self.context,
                WindowsDefenderApplicationControlSupplementalPolicyAssignment,
                ResourcePath("assignments", self.resource_path),
            ),
        )

    @odata(name="deploySummary", navigation=True)
    @property
    def deploy_summary(self) -> WindowsDefenderApplicationControlSupplementalPolicyDeploymentSummary:
        """Gets the deploySummary property"""
        from office365.intune.devices.management.windows_defender_application_control_supplemental_policy_deployment_summary import (  # noqa: E501
            WindowsDefenderApplicationControlSupplementalPolicyDeploymentSummary,
        )

        return self.properties.get(
            "deploySummary",
            WindowsDefenderApplicationControlSupplementalPolicyDeploymentSummary(
                self.context, ResourcePath("deploySummary", self.resource_path)
            ),
        )

    @odata(name="deviceStatuses", navigation=True)
    @property
    def device_statuses(self) -> EntityCollection[WindowsDefenderApplicationControlSupplementalPolicyDeploymentStatus]:
        """Gets the deviceStatuses property"""
        from office365.intune.devices.management.windows_defender_application_control_supplemental_policy_deployment_status import (  # noqa: E501
            WindowsDefenderApplicationControlSupplementalPolicyDeploymentStatus,
        )

        return self.properties.get(
            "deviceStatuses",
            EntityCollection[WindowsDefenderApplicationControlSupplementalPolicyDeploymentStatus](
                self.context,
                WindowsDefenderApplicationControlSupplementalPolicyDeploymentStatus,
                ResourcePath("deviceStatuses", self.resource_path),
            ),
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.WindowsDefenderApplicationControlSupplementalPolicy"

    @require_permission(
        delegated=[
            "DeviceManagementApps.ReadWrite.All",
        ],
        application=[
            "DeviceManagementApps.ReadWrite.All",
        ],
    )
    def assign(
        self,
        wdac_policy_assignments: ClientValueCollection[WindowsDefenderApplicationControlSupplementalPolicyAssignment],
    ) -> Self:
        """assign operation.

        Args:
            wdac_policy_assignments:
                wdacPolicyAssignments parameter
        """
        qry = ServiceOperationQuery(self, "assign", None, {"wdacPolicyAssignments": wdac_policy_assignments}, None, None)
        self.context.add_query(qry)
        return self
