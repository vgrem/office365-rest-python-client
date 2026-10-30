from __future__ import annotations

from typing import Optional

from office365.entity import Entity
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.odata_property import odata
from office365.security.account import Account


class IdentityAccounts(Entity):
    @odata(name="cloudSecurityIdentifier")
    @property
    def cloud_security_identifier(self) -> Optional[str]:
        """Gets the cloudSecurityIdentifier property"""
        return self.properties.get("cloudSecurityIdentifier", None)

    @odata(name="displayName")
    @property
    def display_name(self) -> Optional[str]:
        """Gets the displayName property"""
        return self.properties.get("displayName", None)

    @odata(name="domain")
    @property
    def domain(self) -> Optional[str]:
        """Gets the domain property"""
        return self.properties.get("domain", None)

    @odata(name="isEnabled")
    @property
    def is_enabled(self) -> Optional[bool]:
        """Gets the isEnabled property"""
        return self.properties.get("isEnabled", None)

    @odata(name="onPremisesSecurityIdentifier")
    @property
    def on_premises_security_identifier(self) -> Optional[str]:
        """Gets the onPremisesSecurityIdentifier property"""
        return self.properties.get("onPremisesSecurityIdentifier", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.IdentityAccounts"

    @odata(name="accounts")
    @property
    def accounts(self) -> ClientValueCollection[Account]:
        """Gets the accounts property"""
        return self.properties.get("accounts", ClientValueCollection[Account](Account))
