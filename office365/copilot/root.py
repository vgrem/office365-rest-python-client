from office365.copilot.admin import CopilotAdmin
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity
from office365.teams.aiinteractions.history import AIInteractionHistory


class CopilotRoot(Entity):
    """A container for Microsoft 365 Copilot admin controls."""

    @odata(name="admin", navigation=True)
    @property
    def admin(self) -> CopilotAdmin:
        """The Microsoft 365 Copilot admin who can add or modify Copilot settings. Read-only. Nullable."""
        return self.properties.get(
            "admin",
            CopilotAdmin(self.context, ResourcePath("admin", self.resource_path)),
        )

    @odata(name="interactionHistory", navigation=True)
    @property
    def interaction_history(self) -> AIInteractionHistory:
        """The history of interactions between AI agents and users."""
        return self.properties.get(
            "interactionHistory",
            AIInteractionHistory(self.context, ResourcePath("interactionHistory", self.resource_path)),
        )
