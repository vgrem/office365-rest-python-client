from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class AccessRequestSettings(ClientValue):
    """
    This class returns the access request settings. It's an optional property that can be retrieved in
    Microsoft.SharePoint.Client.Sharing.SecurableObjectExtensions.GetSharingInformation() call on a list item.
    """

    hasPendingAccessRequests: bool | None = None
    pendingAccessRequestsLink: str | None = None
    requiresAccessApproval: bool | None = None

    @property
    def entity_type_name(self):
        return "SP.Sharing.AccessRequestSettings"
