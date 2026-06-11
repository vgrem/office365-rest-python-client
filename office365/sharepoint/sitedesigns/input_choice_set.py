from __future__ import annotations

from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.sitedesigns.input_choice import InputChoice


class InputChoiceSet(ClientValue):
    choices: ClientValueCollection[InputChoice] = field(default_factory=lambda: ClientValueCollection(InputChoice))
    isMultiSelect: bool | None = None
    isRequired: bool | None = None
    style: str | None = None
    value: str | None = None
