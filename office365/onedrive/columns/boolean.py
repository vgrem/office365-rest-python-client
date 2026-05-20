from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class BooleanColumn(ClientValue):
    """The booleanColumn on a columnDefinition resource indicates that the column holds a boolean value"""
