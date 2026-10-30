from __future__ import annotations

from typing import Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata


class AccessPackageTextInputQuestion(Entity):
    @odata(name="isSingleLineQuestion")
    @property
    def is_single_line_question(self) -> Optional[bool]:
        """Gets the isSingleLineQuestion property"""
        return self.properties.get("isSingleLineQuestion", None)

    @odata(name="regexPattern")
    @property
    def regex_pattern(self) -> Optional[str]:
        """Gets the regexPattern property"""
        return self.properties.get("regexPattern", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AccessPackageTextInputQuestion"
