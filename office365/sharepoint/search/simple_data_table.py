from __future__ import annotations

from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.value import value
from office365.sharepoint.search.simple_data_row import SimpleDataRow


@value
class SimpleDataTable(ClientValue):
    """Represents a data table"""

    Rows: ClientValueCollection[SimpleDataRow] = field(default_factory=lambda: ClientValueCollection(SimpleDataRow))

    @property
    def entity_type_name(self):
        return "SP.SimpleDataTable"
