from enum import Enum


class ExchangeIdFormat(Enum):
    entryId = "0"
    ewsId = "1"
    immutableEntryId = "2"
    restId = "3"
    restImmutableEntryId = "4"

    @property
    def entity_type_name(self):
        return "microsoft.graph.ExchangeIdFormat"
