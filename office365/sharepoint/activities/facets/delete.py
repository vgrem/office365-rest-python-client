from __future__ import annotations

from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class DeleteFacet(ClientValue):
    name: Optional[str] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Activities.DeleteFacet"
