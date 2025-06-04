from office365.copilot.admin import CopilotAdmin
from office365.runtime.paths.resource_path import ResourcePath
from office365.sharepoint.entity import Entity


class CopilotRoot(Entity):
    """A container for Microsoft 365 Copilot admin controls."""

    @property
    def admin(self):
        """The Microsoft 365 Copilot admin who can add or modify Copilot settings. Read-only. Nullable."""
        return self.properties.get(
            "admin",
            CopilotAdmin(self.context, ResourcePath("admin", self.resource_path)),
        )
