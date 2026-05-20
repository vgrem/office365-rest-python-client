from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.sharepoint.types.resource_path import ResourcePath as SPResPath


@dataclass
class MoveFacet(ClientValue):
    from_: SPResPath = field(default_factory=SPResPath)
    to: SPResPath = field(default_factory=SPResPath)

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Activities.MoveFacet"
