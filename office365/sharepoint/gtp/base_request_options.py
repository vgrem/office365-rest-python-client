from __future__ import annotations

from typing import Optional


from dataclasses import dataclass
from office365.runtime.client_value import ClientValue


@dataclass
class BaseGptRequestOptions(ClientValue):

    FrequencyPenalty: Optional[float] = None
    MaxTokens: Optional[int] = None
    PresencePenalty: Optional[float] = None
    Stop: Optional[str] = None
    Temperature: Optional[float] = None
    TopP: Optional[float] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Internal.BaseGptRequestOptions"