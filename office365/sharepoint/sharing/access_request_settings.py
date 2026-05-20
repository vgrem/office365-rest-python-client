from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class AccessRequestSettings(ClientValue):
    """
    This class returns the access request settings. It's an optional property that can be retrieved in
    Microsoft.SharePoint.Client.Sharing.SecurableObjectExtensions.GetSharingInformation() call on a list item.

    Fields:
        hasPendingAccessRequests: Boolean indicating whether there are pending access requests for the list item.
        pendingAccessRequestsLink: The full URL to the access requests page for the list item, or an empty string
            if the link is not available.
        requiresAccessApproval: Boolean indicating whether the current user's access on the list item requires
            approval from admin for sharing to others.
    """

    hasPendingAccessRequests: bool | None = None
    pendingAccessRequestsLink: str | None = None
    requiresAccessApproval: bool | None = None

    @property
    def entity_type_name(self):
        return "SP.Sharing.AccessRequestSettings"
