from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class QueryPropertyValue(ClientValue):
    """This object is used to store values of predefined types. The object MUST have a value set for only
    one of the property."""

    BoolVal: bool | None = None
    IntVal: int | None = None
    StrArray: list[str] | None = None
    StrVal: str | None = None
    QueryPropertyValueTypeIndex: int | None = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Client.Search.Query.QueryPropertyValue"
