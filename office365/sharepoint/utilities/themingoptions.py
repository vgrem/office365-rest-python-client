from __future__ import annotations

from dataclasses import field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.utilities.jsontheme import JsonTheme


class ThemingOptions(ClientValue):
    hideDefaultThemes: Optional[bool] = None
    themePreviews: ClientValueCollection[JsonTheme] = field(default_factory=lambda: ClientValueCollection(JsonTheme))

    @property
    def entity_type_name(self):
        return "SP.Utilities.ThemingOptions"
