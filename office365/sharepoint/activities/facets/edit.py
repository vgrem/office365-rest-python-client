from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class EditFacet(ClientValue):
    """"""

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Activities.EditFacet"
