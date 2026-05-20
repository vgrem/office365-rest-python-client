from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class WebInfoCreationInformation(ClientValue):
    Description: Optional[str] = None
    Language: Optional[int] = None
    Title: Optional[str] = None
    Url: Optional[str] = None
    UseUniquePermissions: Optional[bool] = None
    WebTemplate: Optional[str] = None
