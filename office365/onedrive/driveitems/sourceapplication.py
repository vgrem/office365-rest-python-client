from enum import Enum


class DriveItemSourceApplication(Enum):
    teams = "0"
    yammer = "1"
    sharePoint = "2"
    oneDrive = "3"
    stream = "4"
    powerPoint = "5"
    office = "6"
    loki = "7"
    loop = "8"
    other = "9"
    unknownFutureValue = "10"

    @property
    def entity_type_name(self):
        return "microsoft.graph.DriveItemSourceApplication"
