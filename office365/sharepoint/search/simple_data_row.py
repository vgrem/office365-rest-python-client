from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue
from office365.runtime.utilities import parse_key_value_collection


@dataclass
class SimpleDataRow(ClientValue):
    """Represents a row in a data table"""

    Cells: dict | None = None

    def set_property(self, k, v, persist_changes=True):
        self.Cells = parse_key_value_collection(v)
        return self
