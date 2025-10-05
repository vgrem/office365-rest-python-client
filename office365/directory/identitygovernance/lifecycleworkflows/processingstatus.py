from enum import Enum


class LifecycleWorkflowProcessingStatus(Enum):
    queued = "0"
    inProgress = "1"
    completed = "2"
    completedWithErrors = "3"
    canceled = "4"
    failed = "5"
    unknownFutureValue = "6"
