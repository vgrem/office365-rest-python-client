from enum import Enum


class CustomTaskExtensionOperationStatus(Enum):
    none_ = "-1"
    completed = "0"
    failed = "1"
    unknownFutureValue = "2"
