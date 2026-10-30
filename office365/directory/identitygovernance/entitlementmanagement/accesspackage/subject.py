from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from office365.directory.identitygovernance.entitlementmanagement.accesspackage.subject_lifecycle import (  # noqa: E501
    AccessPackageSubjectLifecycle,
)
from office365.directory.identitygovernance.entitlementmanagement.accesspackage.subjecttype import (
    AccessPackageSubjectType,
)
from office365.entity import Entity
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.directory.identitygovernance.entitlementmanagement.connected_organization import (
        ConnectedOrganization,
    )


class AccessPackageSubject(Entity):
    @odata(name="displayName")
    @property
    def display_name(self) -> Optional[str]:
        """Gets the displayName property"""
        return self.properties.get("displayName", None)

    @odata(name="email")
    @property
    def email(self) -> Optional[str]:
        """Gets the email property"""
        return self.properties.get("email", None)

    @odata(name="objectId")
    @property
    def object_id(self) -> Optional[str]:
        """Gets the objectId property"""
        return self.properties.get("objectId", None)

    @odata(name="onPremisesSecurityIdentifier")
    @property
    def on_premises_security_identifier(self) -> Optional[str]:
        """Gets the onPremisesSecurityIdentifier property"""
        return self.properties.get("onPremisesSecurityIdentifier", None)

    @odata(name="principalName")
    @property
    def principal_name(self) -> Optional[str]:
        """Gets the principalName property"""
        return self.properties.get("principalName", None)

    @odata(name="subjectType")
    @property
    def subject_type(self) -> AccessPackageSubjectType:
        """Gets the subjectType property"""
        return self.properties.get("subjectType", AccessPackageSubjectType.notSpecified)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AccessPackageSubject"

    @odata(name="subjectLifecycle")
    @property
    def subject_lifecycle(self) -> AccessPackageSubjectLifecycle:
        """Gets the subjectLifecycle property"""
        return self.properties.get("subjectLifecycle", AccessPackageSubjectLifecycle.notDefined)

    @odata(name="connectedOrganization", navigation=True)
    @property
    def connected_organization(self) -> ConnectedOrganization:
        """Gets the connectedOrganization property"""
        from office365.directory.identitygovernance.entitlementmanagement.connected_organization import (
            ConnectedOrganization,
        )

        return self.properties.get(
            "connectedOrganization",
            ConnectedOrganization(self.context, ResourcePath("connectedOrganization", self.resource_path)),
        )
