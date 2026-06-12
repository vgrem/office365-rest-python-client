from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.brandcenter.theme_data import ThemeData


@dataclass
class TenantThemes(ClientValue):
    hideDefaultThemes: bool | None = None
    themeData: ClientValueCollection[ThemeData] = field(default_factory=lambda: ClientValueCollection(ThemeData))
