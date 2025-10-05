from enum import Enum


class LifecycleTaskCategory(Enum):
    joiner = "1"
    leaver = "2"
    unknownFutureValue = "4"
    mover = "8"
