from __future__ import annotations

from typing import Optional

from office365.runtime.types.collections import StringCollection
from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity


class MultiConditionalAccessPolicy(Entity):
    @odata(name="definition")
    @property
    def definition(self) -> StringCollection:
        """Gets the definition property"""
        return self.properties.get("definition", StringCollection())

    @odata(name="displayName")
    @property
    def display_name(self) -> Optional[str]:
        """Gets the displayName property"""
        return self.properties.get("displayName", None)

    @odata(name="id")
    @property
    def id_(self) -> Optional[str]:
        """Gets the id property"""
        return self.properties.get("id", None)

    @odata(name="isOrganizationDefault")
    @property
    def is_organization_default(self) -> Optional[bool]:
        """Gets the isOrganizationDefault property"""
        return self.properties.get("isOrganizationDefault", None)

    @odata(name="policyIdentifier")
    @property
    def policy_identifier(self) -> Optional[str]:
        """Gets the policyIdentifier property"""
        return self.properties.get("policyIdentifier", None)

    @property
    def entity_type_name(self) -> str:
        return "SP.Directory.MultiConditionalAccessPolicy"

    @odata(name="id")
    @property
    def id(self) -> Optional[str]:
        """Gets the id property"""
        return self.properties.get("id", None)
