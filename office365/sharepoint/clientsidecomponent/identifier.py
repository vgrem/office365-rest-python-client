from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class SPClientSideComponentIdentifier(ClientValue):
    """This identifier uniquely identifies a component."""

    version: str | None = None
    id: str | None = None

    def __repr__(self):
        return self.id or self.entity_type_name

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.ClientSideComponent.SPClientSideComponentIdentifier"
