from __future__ import annotations

from typing import Optional

from office365.directory.identitygovernance.entitlementmanagement.accesspackage.answer_choice import (  # noqa: E501
    AccessPackageAnswerChoice,
)
from office365.entity import Entity
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.odata_property import odata


class AccessPackageMultipleChoiceQuestion(Entity):
    @odata(name="isMultipleSelectionAllowed")
    @property
    def is_multiple_selection_allowed(self) -> Optional[bool]:
        """Gets the isMultipleSelectionAllowed property"""
        return self.properties.get("isMultipleSelectionAllowed", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AccessPackageMultipleChoiceQuestion"

    @odata(name="choices")
    @property
    def choices(self) -> ClientValueCollection[AccessPackageAnswerChoice]:
        """Gets the choices property"""
        return self.properties.get(
            "choices", ClientValueCollection[AccessPackageAnswerChoice](AccessPackageAnswerChoice)
        )
