from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


@dataclass
class ChoiceColumn(ClientValue):
    """
    The choiceColumn on a columnDefinition resource indicates that the column's values can be selected
    from a list of choices.
    """

    allowTextEntry: bool | None = True
    choices: StringCollection = field(default_factory=StringCollection)
    displayAs: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ChoiceColumn"
