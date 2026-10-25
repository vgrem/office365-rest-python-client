from typing import Optional

from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity


class AccessTokenOptionalClaim(Entity):
    @odata(name="Acrs")
    @property
    def acrs(self) -> Optional[str]:
        """Gets the Acrs property"""
        return self.properties.get("Acrs", None)

    @property
    def entity_type_name(self):
        return "SP.OAuth.AccessTokenOptionalClaim"
