from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class WebPartPosition(ClientValue):
    """Represents the position information of the given web part to the current page"""
