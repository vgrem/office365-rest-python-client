from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.search.simple_data_row import SimpleDataRow


@dataclass
class SimpleDataTable(ClientValue):
    """Represents a data table"""

    Rows: ClientValueCollection[SimpleDataRow] = field(default_factory=lambda: ClientValueCollection(SimpleDataRow))

    @property
    def entity_type_name(self):
        return "SP.SimpleDataTable"
