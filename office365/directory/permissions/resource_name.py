from __future__ import annotations

from enum import Enum


class ResourceName(str, Enum):
    """Well-known Entra ID service principal names for permission checks.

    Each member's value is the display name used in the Microsoft Graph
    ``servicePrincipals`` API, so it can be passed directly to
    :func:`~office365.directory.permissions.guard.has_app_permission` and
    :func:`~office365.directory.permissions.guard.has_delegated_permission`.

    Usage:

        .. code-block:: python

            from office365.directory.permissions.guard import has_app_permission
            from office365.directory.permissions.resource_name import ResourceName

            has_app_permission(client, "Sites.Read.All", client_id, ResourceName.SharePoint)
    """

    Graph = "Microsoft Graph"
    SharePoint = "Office 365 SharePoint Online"
    Exchange = "Office 365 Exchange Online"
    Azure = "Azure Service Management"
    Flow = "Power Automate"
    PowerApps = "PowerApps Service"
    Dynamics = "Dynamics CRM"

    def __str__(self) -> str:
        return self.value
