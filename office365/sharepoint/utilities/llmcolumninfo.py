from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class LLMColumnInfo(ClientValue):
    AnalyzeImageDetailLevel: Optional[str] = None
    AnalyzeImageWithVision: Optional[bool] = None
    AutofillColumnType: Optional[str] = None
    CustomModelId: Optional[str] = None
    CustomParametersJson: Optional[str] = None
    IsEnabled: Optional[bool] = None
    Prompt: Optional[str] = None

    @property
    def entity_type_name(self):
        return "SP.Utilities.LLMColumnInfo"
