from enum import Enum


class ApplicationGuardBlockClipboardSharingType(Enum):
    notConfigured = "0"
    blockBoth = "1"
    blockHostToContainer = "2"
    blockContainerToHost = "3"
    blockNone = "4"

    @property
    def entity_type_name(self):
        return "microsoft.graph.ApplicationGuardBlockClipboardSharingType"
