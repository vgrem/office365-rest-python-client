from __future__ import annotations

from dataclasses import dataclass
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

    component_type: str | None = None
    manifest: str | None = None
    manifest_type: str | None = None
    id_: str | None = None
    manifest_activated_time: datetime | None = None
    name: str | None = None
    status: int | None = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.ClientSideComponent.SPClientSideComponentQueryResult"
