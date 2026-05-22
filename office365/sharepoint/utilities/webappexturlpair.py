from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class WebAppExtUrlPair(ClientValue):
    Ext: Optional[str] = None
    WacUrl: Optional[str] = None

    @property
    def entity_type_name(self):
        return "SP.Utilities.WebAppExtUrlPair"
