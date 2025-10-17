from enum import Enum


class ColumnTypes(Enum):
    text = "text"
    "Single line text."
    note = "note"
    "Multiline text."
    choice = "choice"
    "Choice column"
    multichoice = "multichoice"
    "Multichoice column."
    number = "4"
    currency = "5"
    dateTime = "6"
    lookup = "7"
    boolean = "8"
    user = "9"
    url = "10"
    calculated = "11"
    location = "12"
    geolocation = "13"
    term = "14"
    multiterm = "15"
    thumbnail = "16"
    approvalStatus = "17"
    unknownFutureValue = "18"

    @property
    def entity_type_name(self):
        return "microsoft.graph.ColumnTypes"
