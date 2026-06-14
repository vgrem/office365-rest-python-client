from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from office365.runtime.client_value import ClientValue


@dataclass
class SPClientSideComponentQueryResult(ClientValue):
    """This object contains information about the requested component and the status of the query that was used to
    retrieve the component.

    Fields:
        component_type (str | None): Specifies the type of component.
        manifest (str | None):
        manifest_type (str | None):
    """

    ComponentType: int | None = None
    Id: str | None = None
    Manifest: str | None = None
    ManifestActivatedTime: datetime | None = field(default_factory=lambda: datetime.min)
    ManifestType: int | None = None
    Name: str | None = None
    Status: int | None = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.ClientSideComponent.SPClientSideComponentQueryResult"
