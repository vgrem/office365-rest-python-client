from __future__ import annotations

import uuid
from dataclasses import dataclass

from office365.runtime.client_value_collection import ClientValueCollection


@dataclass
class StringCollection(ClientValueCollection[str]):
    """A type-safe collection of string values with OData serialization support."""

    def __init__(self, *args: str):
        super().__init__(item_type=str, _data=list(args) if args else None)


@dataclass
class GuidCollection(ClientValueCollection):
    """A collection of UUID values with proper OData serialization."""

    def __init__(self, *args):
        super().__init__(item_type=uuid.UUID, _data=list(args) if args else None)
