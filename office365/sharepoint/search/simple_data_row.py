from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.runtime.converters.keyvalue import parse_key_value_collection


@dataclass
class SimpleDataRow(ClientValue):
    """Represents a row in a data table"""

    Cells: dict = field(default_factory=dict)

    def get(self, name: str, default=None):
        """Return the value of the cell named ``name`` (``default`` when absent)."""
        return self.Cells.get(name, default)

    def as_dict(self) -> dict:
        """Return the row's cells as a plain ``dict``."""
        return dict(self.Cells)

    def set_property(self, k, v, persist_changes=True):
        self.Cells = parse_key_value_collection(v)
        return self
