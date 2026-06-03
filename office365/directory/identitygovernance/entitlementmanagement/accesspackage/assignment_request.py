from __future__ import annotations

from datetime import datetime
from typing import Optional

from office365.directory.identitygovernance.entitlementmanagement.accesspackage.assignment import AccessPackageAssignment
from office365.directory.identitygovernance.entitlementmanagement.accesspackage.package import AccessPackage
from office365.directory.identitygovernance.entitlementmanagement.accesspackage.requeststate import (
    AccessPackageRequestState,
)
from office365.directory.identitygovernance.entitlementmanagement.accesspackage.requesttype import (
    AccessPackageRequestType,
)
from office365.directory.identitygovernance.entitlementmanagement.accesspackage.subject import AccessPackageSubject
from office365.entity import Entity
from office365.runtime.paths.resource_path import ResourcePath


class AccessPackageAssignmentRequest(Entity):
    @property
    def completed_date_time(self) -> datetime:
        """Gets the completedDateTime property"""
        return self.properties.get("completedDateTime", datetime.min)

    @property
    def created_date_time(self) -> datetime:
        """Gets the createdDateTime property"""
        return self.properties.get("createdDateTime", datetime.min)

    @property
    def justification(self) -> Optional[str]:
        """Gets the justification property"""
        return self.properties.get("justification", None)

    @property
    def request_type(self) -> AccessPackageRequestType:
        """Gets the requestType property"""
        return self.properties.get("requestType", AccessPackageRequestType.notSpecified)

    @property
    def state(self) -> AccessPackageRequestState:
        """Gets the state property"""
        return self.properties.get("state", AccessPackageRequestState.submitted)

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
    def assignment(self) -> AccessPackageAssignment:
        """Gets the assignment property"""
        return self.properties.get(
            "assignment", AccessPackageAssignment(self.context, ResourcePath("assignment", self.resource_path))
        )

    @property
    def requestor(self) -> AccessPackageSubject:
        """Gets the requestor property"""
        return self.properties.get(
            "requestor", AccessPackageSubject(self.context, ResourcePath("requestor", self.resource_path))
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AccessPackageAssignmentRequest"
