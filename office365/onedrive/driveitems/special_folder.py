from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class SpecialFolder(ClientValue):
    """The SpecialFolder resource groups special folder-related data items into a single structure."""

    name: str | None = None
