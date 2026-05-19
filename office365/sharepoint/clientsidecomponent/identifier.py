from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue


@dataclass
class SPClientSideComponentIdentifier(ClientValue):
    """This identifier uniquely identifies a component."""

    id_: str | None = field(default=None)
    version: str | None = None

    def __post_init__(self):
        self.id = self.id_

    def __repr__(self):
        return self.id or self.entity_type_name

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.ClientSideComponent.SPClientSideComponentIdentifier"
