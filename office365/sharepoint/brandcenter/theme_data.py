from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class ThemeData(ClientValue):
    name: Optional[str] = None
    source: Optional[str] = None
    isThemesV2: Optional[bool] = None
    themeJson: Optional[str] = None
    id: Optional[int] = None
    isVisible: Optional[bool] = None
