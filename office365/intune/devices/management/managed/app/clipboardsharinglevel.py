from enum import Enum


class ManagedAppClipboardSharingLevel(Enum):
    allApps = "0"
    managedAppsWithPasteIn = "1"
    managedApps = "2"
    blocked = "3"

    @property
    def entity_type_name(self):
        return "microsoft.graph.ManagedAppClipboardSharingLevel"
