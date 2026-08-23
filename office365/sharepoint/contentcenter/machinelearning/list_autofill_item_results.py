from __future__ import annotations

from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection


class SPMachineLearningListAutofillItemResults(ClientValue):
    Failed: ClientValueCollection = field(default_factory=ClientValueCollection)
    NothingToDo: ClientValueCollection = field(default_factory=ClientValueCollection)
    NoUsableValue: ClientValueCollection = field(default_factory=ClientValueCollection)
    Queued: ClientValueCollection = field(default_factory=ClientValueCollection)
    Succeeded: ClientValueCollection = field(default_factory=ClientValueCollection)

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.Office.Server.ContentCenter.SPMachineLearningListAutofillItemResults"
