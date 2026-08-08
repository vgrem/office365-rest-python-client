from __future__ import annotations

from enum import Enum


class TimeOffReasonIconType(Enum):
    none = "0"
    car = "1"
    calendar = "2"
    running = "3"
    plane = "4"
    firstAid = "5"
    doctor = "6"
    notWorking = "7"
    clock = "8"
    juryDuty = "9"
    globe = "10"
    cup = "11"
    phone = "12"
    weather = "13"
    umbrella = "14"
    piggyBank = "15"
    dog = "16"
    cake = "17"
    trafficCone = "18"
    pin = "19"
    sunny = "20"
    unknownFutureValue = "21"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.TimeOffReasonIconType"
