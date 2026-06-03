from __future__ import annotations

from datetime import timedelta

from office365.directory.identitygovernance.entitlementmanagement.accesspackage.externaluserlifecycleaction import (
    AccessPackageExternalUserLifecycleAction,
)
from office365.entity import Entity


class EntitlementManagementSettings(Entity):
    @property
    def duration_until_external_user_deleted_after_blocked(self) -> timedelta:
        """Gets the durationUntilExternalUserDeletedAfterBlocked property"""
        return self.properties.get("durationUntilExternalUserDeletedAfterBlocked", timedelta.min)

    @property
    def external_user_lifecycle_action(self) -> AccessPackageExternalUserLifecycleAction:
        """Gets the externalUserLifecycleAction property"""
        return self.properties.get("externalUserLifecycleAction", AccessPackageExternalUserLifecycleAction.none)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.EntitlementManagementSettings"
