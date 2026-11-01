"""The directory roles this library names, so a role is spelled once and checked by name.

A declaration can state a role as an *alternative*: holding it satisfies the call where the
permission alone does not decide, which is how tenant-wide SharePoint operations are granted. The
string it states is compared, unchanged, against the ``displayName`` the tenant's directory
answers - so it has to be spelled exactly as Entra spells it.

Misspelled, it does not fail, it names a role nobody holds. The requirement is then simply never
met, and because a SharePoint-only client cannot read the role list at all, the answer becomes
*unprovable*, which passes. Both directions hide the typo, and a literal repeated at every call
site is a chance to make one each time.

These are the roles this library and its tests mention, not Entra's catalogue: there are hundreds
of built-in roles and Microsoft keeps adding to them, so ``role=`` still takes a plain string for
any name not listed here.

This module is pure: a vocabulary, no client, no request.
"""

from __future__ import annotations

from enum import Enum


class DirectoryRole(str, Enum):
    """A directory role, named as its ``displayName`` is.

    Usage::

        from office365.permissions import DirectoryRole
        from office365.sharepoint.permissions import SiteLevel, site_access


        @site_access(SiteLevel.FULL_CONTROL, role=DirectoryRole.SharePointAdministrator)
        def register_hub_site(self): ...
    """

    SharePointAdministrator = "SharePoint Administrator"
    GlobalAdministrator = "Global Administrator"
    PrivilegedRoleAdministrator = "Privileged Role Administrator"
    ComplianceAdministrator = "Compliance Administrator"
    ComplianceDataAdministrator = "Compliance Data Administrator"
    RecordsManagement = "Records Management"

    def __str__(self) -> str:
        return self.value
