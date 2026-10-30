from __future__ import annotations

from typing import TYPE_CHECKING

from office365.directory.identitygovernance.entitlementmanagement.accesspackage.suggestion_reason import (  # noqa: E501
    AccessPackageSuggestionReason,
)
from office365.entity import Entity
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.directory.identitygovernance.entitlementmanagement.available_access_package import (
        AvailableAccessPackage,
    )


class AccessPackageSuggestion(Entity):
    @odata(name="reasons")
    @property
    def reasons(self) -> ClientValueCollection[AccessPackageSuggestionReason]:
        """Gets the reasons property"""
        return self.properties.get(
            "reasons", ClientValueCollection[AccessPackageSuggestionReason](AccessPackageSuggestionReason)
        )

    @odata(name="accessPackage", navigation=True)
    @property
    def access_package(self) -> AvailableAccessPackage:
        """Gets the accessPackage property"""
        from office365.directory.identitygovernance.entitlementmanagement.available_access_package import (
            AvailableAccessPackage,
        )

        return self.properties.get(
            "accessPackage", AvailableAccessPackage(self.context, ResourcePath("accessPackage", self.resource_path))
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AccessPackageSuggestion"
