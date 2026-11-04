from __future__ import annotations

from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class JsonTheme(ClientValue):
    name: Optional[str] = None
    themeJson: Optional[str] = None

    @property
    def entity_type_name(self):
        return "SP.Utilities.JsonTheme"
