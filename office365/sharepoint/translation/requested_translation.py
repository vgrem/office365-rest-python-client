from dataclasses import dataclass, field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.sharepoint.types.resource_path import ResourcePath


@dataclass
class RequestedTranslation(ClientValue):
    LanguageCode: Optional[str] = None
    WebRelativePath: ResourcePath = field(default_factory=ResourcePath)
