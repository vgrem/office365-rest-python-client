from __future__ import annotations

from typing import Optional

from office365.runtime.types.odata_property import odata
from office365.sharepoint.publishing.customproperties.base import BaseCustomProperty


class BigIntCustomProperty(BaseCustomProperty):
    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.SharePoint.Publishing.RestOnly.BigIntCustomProperty"

    @odata(name="Value")
    @property
    def value(self) -> Optional[int]:
        """Gets the Value property"""
        return self.properties.get("Value", None)
