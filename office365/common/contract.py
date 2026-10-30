from __future__ import annotations

from typing import Optional
from uuid import UUID

from office365.entity import Entity
from office365.runtime.types.odata_property import odata


class Contract(Entity):
    @odata(name="contractType")
    @property
    def contract_type(self) -> Optional[str]:
        """Gets the contractType property"""
        return self.properties.get("contractType", None)

    @odata(name="customerId")
    @property
    def customer_id(self) -> Optional[UUID]:
        """Gets the customerId property"""
        return self.properties.get("customerId", None)

    @odata(name="defaultDomainName")
    @property
    def default_domain_name(self) -> Optional[str]:
        """Gets the defaultDomainName property"""
        return self.properties.get("defaultDomainName", None)

    @odata(name="displayName")
    @property
    def display_name(self) -> Optional[str]:
        """Gets the displayName property"""
        return self.properties.get("displayName", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.Contract"
