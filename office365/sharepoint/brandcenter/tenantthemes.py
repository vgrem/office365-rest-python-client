from dataclasses import dataclass, field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.brandcenter.theme_data import ThemeData


@dataclass
class TenantThemes(ClientValue):
    hide_default_themes: Optional[bool] = None
    theme_data: ClientValueCollection[ThemeData] = field(default_factory=lambda: ClientValueCollection(ThemeData))
