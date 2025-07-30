from enum import Enum


class BehaviorDuringRetentionPeriod(Enum):
    """ """

    none = "-1"

    doNotRetain = "0"

    retainAsRecord = "2"

    unknownFutureValue = "4"


class DefaultRecordBehavior(Enum):
    """ """

    startLocked = "0"

    startUnlocked = "1"

    unknownFutureValue = "2"


class ActionAfterRetentionPeriod(Enum):
    """ """

    none = "0"

    delete = "1"
