from __future__ import annotations

from typing import Optional


from dataclasses import dataclass, field
from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.utilities.jsontheme import JsonTheme


@dataclass
class ThemingOptions(ClientValue):

    hideDefaultThemes: Optional[bool] = None
    themePreviews: ClientValueCollection[JsonTheme] = field(
        default_factory=lambda: ClientValueCollection(JsonTheme)
    )

    @property
    def entity_type_name(self):
        return "SP.Utilities.ThemingOptions"