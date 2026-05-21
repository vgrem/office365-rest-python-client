from __future__ import annotations

from typing import Optional


from dataclasses import dataclass
from office365.runtime.client_value import ClientValue


@dataclass
class WebCreationInformation(ClientValue):

    """Represents metadata about site creation."""

    Title: Optional[str] = None
    Url: Optional[str] = None
    Description: Optional[str] = None
    Language: Optional[int] = None
    UseSamePermissionsAsParentSite: Optional[bool] = None
    WebTemplate: Optional[str] = None

    @property
    def entity_type_name(self):
        return "SP.WebCreationInformation"