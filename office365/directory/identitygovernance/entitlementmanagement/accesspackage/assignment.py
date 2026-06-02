from __future__ import annotations

from datetime import datetime
from typing import Optional

from office365.directory.identitygovernance.entitlementmanagement.accesspackage.assignment_policy import (
    AccessPackageAssignmentPolicy,
)
from office365.directory.identitygovernance.entitlementmanagement.accesspackage.assignmentstate import (
    AccessPackageAssignmentState,
)
from office365.directory.identitygovernance.entitlementmanagement.accesspackage.package import AccessPackage
from office365.directory.identitygovernance.entitlementmanagement.accesspackage.subject import AccessPackageSubject
from office365.entity import Entity
from office365.runtime.paths.resource_path import ResourcePath


class AccessPackageAssignment(Entity):
    @property
    def expired_date_time(self) -> datetime:
        """Gets the expiredDateTime property"""
        return self.properties.get("expiredDateTime", datetime.min)

    @property
    def state(self) -> AccessPackageAssignmentState:
        """Gets the state property"""
        return self.properties.get("state", AccessPackageAssignmentState.delivering)

    @property
    def status(self) -> Optional[str]:
        """Gets the status property"""
        return self.properties.get("status", None)

    @property
    def access_package(self) -> AccessPackage:
        """Gets the accessPackage property"""
        return self.properties.get(
            "accessPackage", AccessPackage(self.context, ResourcePath("accessPackage", self.resource_path))
        )

    @property
    def assignment_policy(self) -> AccessPackageAssignmentPolicy:
        """Gets the assignmentPolicy property"""
        return self.properties.get(
            "assignmentPolicy",
            AccessPackageAssignmentPolicy(self.context, ResourcePath("assignmentPolicy", self.resource_path)),
        )

    @property
    def target(self) -> AccessPackageSubject:
        """Gets the target property"""
        return self.properties.get(
            "target", AccessPackageSubject(self.context, ResourcePath("target", self.resource_path))
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AccessPackageAssignment"
