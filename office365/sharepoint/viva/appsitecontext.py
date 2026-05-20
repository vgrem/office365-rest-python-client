from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class AppSiteContext(ClientValue):
    site_url: Optional[str] = None
