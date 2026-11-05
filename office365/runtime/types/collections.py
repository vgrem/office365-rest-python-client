from __future__ import annotations

import uuid

from office365.runtime.client_value_collection import ClientValueCollection


class StringCollection(ClientValueCollection[str]):
    """A type-safe collection of string values with OData serialization support."""

    def __init__(self, initial: list[str] | None = None) -> None:
        super().__init__(item_type=str, _data=initial)


class GuidCollection(ClientValueCollection):
    """A collection of UUID values with proper OData serialization."""

    def __init__(self, initial: list | None = None) -> None:
        super().__init__(item_type=uuid.UUID, _data=initial)
