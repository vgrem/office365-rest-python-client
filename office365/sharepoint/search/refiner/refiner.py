from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.search.refiner.entry import RefinerEntry


@dataclass
class Refiner(ClientValue):
    """A refiner contains a list with entries, of the RefinerEntry types"""

    Entries: ClientValueCollection[RefinerEntry] = field(default_factory=lambda: ClientValueCollection(RefinerEntry))
    Name: str | None = None

    @property
    def entity_type_name(self):
        return "Microsoft.Office.Server.Search.REST.Refiner"
