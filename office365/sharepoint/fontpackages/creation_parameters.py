from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class FontPackageCreationParameters(ClientValue):
    IsHidden: Optional[bool] = None
    PackageJson: Optional[str] = None
    Title: Optional[str] = None
