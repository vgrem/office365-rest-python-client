from __future__ import annotations

from typing import Optional

from office365.entity import Entity
from office365.runtime.types.json import Json
from office365.runtime.types.odata_property import odata


class WorkbookFunctionResult(Entity):
    """"""

    @odata(name="value")
    @property
    def value(self) -> Optional[Json]:
        return self.properties.get("value", None)

    @odata(name="error")
    @property
    def error(self) -> Optional[str]:
        """Gets the error property"""
        return self.properties.get("error", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.WorkbookFunctionResult"
