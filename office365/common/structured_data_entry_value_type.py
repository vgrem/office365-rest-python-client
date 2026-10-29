from __future__ import annotations

from enum import Enum


class StructuredDataEntryValueType(Enum):
    dateTime = "0"
    boolean = "1"
    byte = "2"
    string = "3"
    integer32 = "4"
    unsignedInteger32 = "5"
    integer64 = "6"
    unsignedInteger64 = "7"
    stringArray = "8"
    byteArray = "9"
    unknownFutureValue = "10"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.StructuredDataEntryValueType"
