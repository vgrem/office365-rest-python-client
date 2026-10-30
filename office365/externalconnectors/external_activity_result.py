from __future__ import annotations

from office365.entity import Entity
from office365.runtime.types.odata_property import odata
from office365.runtime.types.public_error import PublicError


class ExternalActivityResult(Entity):
    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.externalConnectors.ExternalActivityResult"

    @odata(name="error")
    @property
    def error(self) -> PublicError:
        """Gets the error property"""
        return self.properties.get("error", PublicError())
