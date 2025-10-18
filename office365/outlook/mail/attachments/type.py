from enum import Enum


class AttachmentType(Enum):
    file = "file"
    item = "item"
    reference = "reference"

    @property
    def entity_type_name(self):
        return "microsoft.graph.AttachmentType"
