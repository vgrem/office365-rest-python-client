from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class KnowledgeHubSiteReference(ClientValue):
    site_id: Optional[str] = None
    url: Optional[str] = None
    web_id: Optional[str] = None
