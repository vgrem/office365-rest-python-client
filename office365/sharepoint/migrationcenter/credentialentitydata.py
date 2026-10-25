from __future__ import annotations

from typing import Optional

from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity


class MigrationCredentialEntityData(Entity):
    @odata(name="AccountName")
    @property
    def account_name(self) -> Optional[str]:
        """Gets the AccountName property"""
        return self.properties.get("AccountName", None)

    @odata(name="Description")
    @property
    def description(self) -> Optional[str]:
        """Gets the Description property"""
        return self.properties.get("Description", None)

    @odata(name="Password")
    @property
    def password(self) -> Optional[str]:
        """Gets the Password property"""
        return self.properties.get("Password", None)

    @odata(name="Type")
    @property
    def type_(self) -> Optional[int]:
        """Gets the Type property"""
        return self.properties.get("Type", None)

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.MigrationCenter.Common.MigrationCredentialEntityData"

    @odata(name="Type")
    @property
    def type(self) -> Optional[int]:
        """Gets the Type property"""
        return self.properties.get("Type", None)
