from enum import Enum


class SensitivityLabelAssignmentMethod(Enum):
    standard = "standard"
    """The assignment method for the label is standard."""

    privileged = "privileged"

    auto = "auto"

    unknownFutureValue = "unknownFutureValue"
