from __future__ import annotations

from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


class SPMachineLearningColumnAutofillChoiceSettings(ClientValue):
    Choices: StringCollection = field(default_factory=StringCollection)
    FillInChoice: bool | None = None

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.Office.Server.ContentCenter.SPMachineLearningColumnAutofillChoiceSettings"
