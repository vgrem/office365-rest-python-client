"""The API a permission name belongs to, because a name only means something next to one.

``Sites.ReadWrite.All`` granted on Microsoft Graph and ``Sites.ReadWrite.All`` granted on
SharePoint are two different grants, on two different service principals, unlocking two
different sets of endpoints - and ``Mail.Send`` is an application permission on Graph while the
same string is a delegated permission on Exchange Online. A declaration therefore names the
name *and* the resource it belongs to, and the values below are the display names
``servicePrincipals`` answers to.

This module is pure: a vocabulary, no client, no request.
"""

from __future__ import annotations

from enum import Enum


class ResourceName(str, Enum):
    """An API resource that can grant permissions, named as its service principal is.

    Usage::

        from office365.directory.permissions.guard import has_delegated_permission
        from office365.permissions import ResourceName

        if has_delegated_permission(client, "Sites.Read.All", client_id, ResourceName.SharePoint):
            download_file()
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
