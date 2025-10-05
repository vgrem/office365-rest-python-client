from enum import Enum


class WorkbookOperationStatus(Enum):
    """"""

    notStarted = "0"
    running = "1"
    succeeded = "2"
    failed = "3"
