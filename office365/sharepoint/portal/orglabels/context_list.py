from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.portal.orglabels.context import OrgLabelsContext


@dataclass
class OrgLabelsContextList(ClientValue):
    IsLastPage: bool | None = None
    Labels: ClientValueCollection[OrgLabelsContext] = field(
        default_factory=lambda: ClientValueCollection(OrgLabelsContext)
    )

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Portal.OrgLabelsContextList"
