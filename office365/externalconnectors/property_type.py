from __future__ import annotations

from enum import Enum


class PropertyType(Enum):
    string = "0"
    int64 = "1"
    double = "2"
    dateTime = "3"
    boolean = "4"
    stringCollection = "5"
    int64Collection = "6"
    doubleCollection = "7"
    dateTimeCollection = "8"
    unknownFutureValue = "9"
    principal = "10"
    principalCollection = "11"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.externalConnectors.PropertyType"
