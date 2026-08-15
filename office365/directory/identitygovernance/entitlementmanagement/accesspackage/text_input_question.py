from __future__ import annotations

from typing import Optional

from office365.entity import Entity


class AccessPackageTextInputQuestion(Entity):
    @property
    def is_single_line_question(self) -> Optional[bool]:
        """Gets the isSingleLineQuestion property"""
        return self.properties.get("isSingleLineQuestion", None)

    @property
    def regex_pattern(self) -> Optional[str]:
        """Gets the regexPattern property"""
        return self.properties.get("regexPattern", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AccessPackageTextInputQuestion"
