from enum import Enum


class ExternalSharingSiteOption(Enum):
    """Defines the options for sharing a site with external users."""

    View = "View"
    Edit = "Edit"
    Owner = "Owner"

    @property
    def description(self) -> str:
        """Human-readable description of the sharing option."""
        descriptions = {
            ExternalSharingSiteOption.View: "Provides sharing to AssociatedVisitorGroup",
            ExternalSharingSiteOption.Edit: "Provides sharing to AssociatedMemberGroup",
            ExternalSharingSiteOption.Owner: "Provides sharing to AssociatedOwnerGroup",
        }
        return descriptions[self]
