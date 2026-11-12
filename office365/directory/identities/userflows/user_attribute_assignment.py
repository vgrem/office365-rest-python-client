from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from office365.directory.identities.userflows.attributeinputtype import IdentityUserFlowAttributeInputType
from office365.directory.identities.userflows.user_attribute_values_item import UserAttributeValuesItem
from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.directory.identities.userflows.attribute import (
        IdentityUserFlowAttribute,
    )


class IdentityUserFlowAttributeAssignment(Entity):
    """Update the properties of a identityUserFlowAttributeAssignment object."""

    @odata(name="displayName")
    @property
    def display_name(self) -> Optional[str]:
        """Gets the displayName property"""
        return self.properties.get("displayName", None)

    @odata(name="isOptional")
    @property
    def is_optional(self) -> Optional[bool]:
        """Gets the isOptional property"""
        return self.properties.get("isOptional", None)

    @odata(name="requiresVerification")
    @property
    def requires_verification(self) -> Optional[bool]:
        """Gets the requiresVerification property"""
        return self.properties.get("requiresVerification", None)

    @odata(name="userAttributeValues")
    @property
    def user_attribute_values(self) -> ClientValueCollection[UserAttributeValuesItem]:
        """Gets the userAttributeValues property"""
        return self.properties.get(
            "userAttributeValues", ClientValueCollection[UserAttributeValuesItem](UserAttributeValuesItem)
        )

    @odata(name="userInputType")
    @property
    def user_input_type(self) -> IdentityUserFlowAttributeInputType:
        """Gets the userInputType property"""
        return self.properties.get("userInputType", IdentityUserFlowAttributeInputType.textBox)

    @odata(name="userAttribute", navigation=True)
    @property
    def user_attribute(self) -> IdentityUserFlowAttribute:
        """Gets the userAttribute property"""
        from office365.directory.identities.userflows.attribute import (
            IdentityUserFlowAttribute,
        )

        return self.properties.get(
            "userAttribute", IdentityUserFlowAttribute(self.context, ResourcePath("userAttribute", self.resource_path))
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.IdentityUserFlowAttributeAssignment"


class IdentityUserFlowAttributeAssignmentCollection(EntityCollection[IdentityUserFlowAttributeAssignment]):
    def __init__(self, context, resource_path=None):
        super().__init__(context, IdentityUserFlowAttributeAssignment, resource_path)
