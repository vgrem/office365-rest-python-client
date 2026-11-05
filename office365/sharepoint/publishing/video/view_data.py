from typing import Any

from office365.runtime.client_value import ClientValue


class ViewData(ClientValue):
    TotalHits: Any = None
    TotalUsers: Any = None

    @property
    def entity_type_name(self):
        return "SP.Publishing.ViewData"
