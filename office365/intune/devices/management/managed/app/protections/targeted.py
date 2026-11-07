from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from typing_extensions import Self

from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.intune.devices.management.managed.app.protections.targeted_managed_app_policy_assignment import (
        TargetedManagedAppPolicyAssignment,
    )


class TargetedManagedAppProtection(Entity):
    @odata(name="isAssigned")
    @property
    def is_assigned(self) -> Optional[bool]:
        """Gets the isAssigned property"""
        return self.properties.get("isAssigned", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.TargetedManagedAppProtection"

    @odata(name="assignments", navigation=True)
    @property
    def assignments(self) -> EntityCollection[TargetedManagedAppPolicyAssignment]:
        """Gets the assignments property"""
        from office365.intune.devices.management.managed.app.protections.targeted_managed_app_policy_assignment import (
            TargetedManagedAppPolicyAssignment,
        )

        return self.properties.get(
            "assignments",
            EntityCollection[TargetedManagedAppPolicyAssignment](
                self.context, TargetedManagedAppPolicyAssignment, ResourcePath("assignments", self.resource_path)
            ),
        )

    def assign(self, assignments: ClientValueCollection[TargetedManagedAppPolicyAssignment]) -> Self:
        """assign operation.

        Args:
            assignments (ClientValueCollection[TargetedManagedAppPolicyAssignment]):
                assignments parameter
        """
        qry = ServiceOperationQuery(self, "assign", None, {"assignments": assignments}, None, None)
        self.context.add_query(qry)
        return self
