from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class Hashes(ClientValue):
    """The Hashes resource groups available hashes into a single structure for an item."""
