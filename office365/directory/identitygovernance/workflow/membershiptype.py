from enum import Enum


class MembershipChangeType(Enum):
    add = "1"
    remove = "2"
    unknownFutureValue = "3"
