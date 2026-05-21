from dataclasses import dataclass
from typing import Any

from office365.runtime.client_value import ClientValue


@dataclass
class ViewData(ClientValue):
    TotalHits: Any = None
    TotalUsers: Any = None

    @property
    def entity_type_name(self):
        return "SP.Publishing.ViewData"
