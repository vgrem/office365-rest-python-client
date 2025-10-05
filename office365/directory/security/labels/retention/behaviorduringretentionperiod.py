from enum import Enum


class BehaviorDuringRetentionPeriod(Enum):
    """ """

    none = "-1"

    doNotRetain = "0"

    retainAsRecord = "2"

    unknownFutureValue = "4"
