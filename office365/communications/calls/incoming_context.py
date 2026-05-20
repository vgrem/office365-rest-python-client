from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class IncomingContext(ClientValue):
    """Represents the context associated with an incoming call."""
