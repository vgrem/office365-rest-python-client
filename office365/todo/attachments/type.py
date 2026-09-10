from enum import Enum


class AttachmentType(Enum):
    """The type of a Microsoft To Do attachment."""

    file = "file"
    item = "item"
    reference = "reference"
    unknownFutureValue = "unknownFutureValue"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.attachmentType"
