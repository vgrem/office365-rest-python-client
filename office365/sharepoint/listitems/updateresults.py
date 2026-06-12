from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.listitems.form_update_value import ListItemFormUpdateValue


@dataclass
class ListItemUpdateResults(ClientValue):
    UpdatedData: str | None = None
    UpdateResults: ClientValueCollection[ListItemFormUpdateValue] = field(
        default_factory=lambda: ClientValueCollection(ListItemFormUpdateValue)
    )
