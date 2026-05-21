from __future__ import annotations

import uuid
from dataclasses import dataclass

from office365.runtime.client_value_collection import ClientValueCollection


@dataclass
class StringCollection(ClientValueCollection[str]):
    """A type-safe collection of string values with OData serialization support."""

    def __post_init__(self):
        self._item_type = str


@dataclass
class GuidCollection(ClientValueCollection):
    """A collection of UUID values with proper OData serialization."""

    def __post_init__(self):
        self._item_type = uuid.UUID
