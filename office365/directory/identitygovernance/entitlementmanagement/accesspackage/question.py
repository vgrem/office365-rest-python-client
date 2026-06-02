from __future__ import annotations

from typing import Optional

from office365.entity import Entity


class AccessPackageQuestion(Entity):
    @property
    def is_answer_editable(self) -> Optional[bool]:
        """Gets the isAnswerEditable property"""
        return self.properties.get("isAnswerEditable", None)

    @property
    def is_required(self) -> Optional[bool]:
        """Gets the isRequired property"""
        return self.properties.get("isRequired", None)

    @property
    def sequence(self) -> Optional[int]:
        """Gets the sequence property"""
        return self.properties.get("sequence", None)

    @property
    def text(self) -> Optional[str]:
        """Gets the text property"""
        return self.properties.get("text", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AccessPackageQuestion"
