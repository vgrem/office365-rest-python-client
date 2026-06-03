from __future__ import annotations

from typing import Optional

from office365.entity import Entity


class AccessPackageMultipleChoiceQuestion(Entity):
    @property
    def is_multiple_selection_allowed(self) -> Optional[bool]:
        """Gets the isMultipleSelectionAllowed property"""
        return self.properties.get("isMultipleSelectionAllowed", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AccessPackageMultipleChoiceQuestion"
