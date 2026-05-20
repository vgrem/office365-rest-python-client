from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class OnlineMeetingRestricted(ClientValue):
    """Indicates the reason or reasons media content from a participant is restricted."""
