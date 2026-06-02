from __future__ import annotations

from typing import Optional

from office365.directory.identitygovernance.entitlementmanagement.accesspackage.subjecttype import (
    AccessPackageSubjectType,
)
from office365.entity import Entity


class AccessPackageSubject(Entity):
    @property
    def display_name(self) -> Optional[str]:
        """Gets the displayName property"""
        return self.properties.get("displayName", None)

    @property
    def email(self) -> Optional[str]:
        """Gets the email property"""
        return self.properties.get("email", None)

    @property
    def object_id(self) -> Optional[str]:
        """Gets the objectId property"""
        return self.properties.get("objectId", None)

    @property
    def on_premises_security_identifier(self) -> Optional[str]:
        """Gets the onPremisesSecurityIdentifier property"""
        return self.properties.get("onPremisesSecurityIdentifier", None)

    @property
    def principal_name(self) -> Optional[str]:
        """Gets the principalName property"""
        return self.properties.get("principalName", None)

    @property
    def subject_type(self) -> AccessPackageSubjectType:
        """Gets the subjectType property"""
        return self.properties.get("subjectType", AccessPackageSubjectType.notSpecified)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AccessPackageSubject"
