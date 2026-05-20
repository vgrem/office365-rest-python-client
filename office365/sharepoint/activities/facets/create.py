from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class CreateFacet(ClientValue):
    """"""

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Activities.CreateFacet"
