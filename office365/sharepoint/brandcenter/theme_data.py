from __future__ import annotations

from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class ThemeData(ClientValue):
    name: Optional[str] = None
    source: Optional[str] = None
    isThemesV2: Optional[bool] = None
    themeJson: Optional[str] = None
    id: Optional[int] = None
    isVisible: Optional[bool] = None
    editable: bool | None = None
