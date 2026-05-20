from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class AlterationOptions(ClientValue):
    """Provides the search alteration options for spelling correction."""
