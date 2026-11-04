from typing import Any

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class ViewData(ClientValue):
    TotalHits: Any = None
    TotalUsers: Any = None

    @property
    def entity_type_name(self):
        return "SP.Publishing.ViewData"
