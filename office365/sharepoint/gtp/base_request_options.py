from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class BaseGptRequestOptions(ClientValue):
    FrequencyPenalty: Optional[float] = None
    MaxTokens: Optional[int] = None
    PresencePenalty: Optional[float] = None
    Stop: Optional[str] = None
    Temperature: Optional[float] = None
    TopP: Optional[float] = None
    MaxCompletionTokens: int | None = None
    ReasoningEffort: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.SharePoint.Internal.BaseGptRequestOptions"
