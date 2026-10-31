"""SharePoint's permission ladder, so a method declares a level and not eight names.

SharePoint does not grant endpoint by endpoint the way Microsoft Graph does. It grants a
*permission level* on a site, and the levels nest: something granted ``AllSites.FullControl``
can also manage, and something granted ``AllSites.Manage`` can also write and read. A call
therefore names the weakest level that covers it, and the levels above it as alternatives -
which is why each rung below is spelled with the stronger names beside it rather than alone.

The two flows are named separately because app-only uses different strings for the same rights
(``Sites.Read.All`` where a signed-in user needs ``AllSites.Read``), and a name is only
checkable against the flow the call actually runs under.

:func:`site_access` exists so that the 2,000 methods under :mod:`office365.sharepoint` say one
word instead of repeating six lines and the resource name:

    @site_access(SiteLevel.WRITE)
    def add_item(self, item_creation_information): ...

The level is a claim about the *weakest* grant that works, so an endpoint that only reads
declares ``READ`` even though ``MANAGE`` would satisfy it: over-claiming makes a live test skip
on a tenant that could have run it.

A few operations reach past one site collection - the migration API, bring-your-own-key, hub
site registration - and no rung covers them on its own: they also want the caller to be a
SharePoint Administrator. Those pass ``role="SharePoint Administrator"``, which declares the
role as the alternative it is rather than as another name to grant:

    @site_access(SiteLevel.FULL_CONTROL, role="SharePoint Administrator")
"""

from __future__ import annotations

from enum import Enum
from typing import Callable, Optional, TypeVar

from office365.permissions import ResourceName, require_permission

F = TypeVar("F", bound=Callable[..., object])

#: Delegated names per rung, weakest first: rung *n* needs one of the names from *n* on.
_DELEGATED = ("AllSites.Read", "AllSites.Write", "AllSites.Manage", "AllSites.FullControl")

#: The app-only equivalent of the same four rungs, in the same order.
_APPLICATION = ("Sites.Read.All", "Sites.ReadWrite.All", "Sites.Manage.All", "Sites.FullControl.All")


class SiteLevel(int, Enum):
    """A rung of the site-permission ladder: the value is its position, weakest at zero."""

    #: Read items, lists, webs and pages.
    READ = 0
    #: Everything ``READ`` does, and editing list items: documents, pages' content, versions.
    WRITE = 1
    #: Everything ``WRITE`` does, and the list itself: its schema, rules, forms, views,
    #: permissions and sharing links.
    MANAGE = 2
    #: Everything ``MANAGE`` does, and the site collection: features, themes, navigation,
    #: language settings, site templates.
    FULL_CONTROL = 3

    @property
    def delegated(self) -> tuple[str, ...]:
        """The user scopes that grant this rung, weakest first."""
        return _DELEGATED[self.value :]

    @property
    def application(self) -> tuple[str, ...]:
        """The app-only permissions that grant this rung, weakest first."""
        return _APPLICATION[self.value :]


def site_access(level: SiteLevel, role: Optional[str] = None) -> Callable[[F], F]:
    """Declare a SharePoint call as needing ``level``, or any rung above it.

    ``role`` names an Entra ID directory role that also satisfies the call - the escape hatch
    for an operation that reaches past the site collection, where the permission alone does not
    decide. Holding it satisfies the whole declaration, so it is stated as an alternative and
    never as a name to grant.

    Thin on purpose: it fills in the two flow names and the resource, and hands the rest to
    :func:`~office365.permissions.declaration.require_permission`, which owns what a
    declaration *is*.
    """
    return require_permission(
        delegated=level.delegated,
        application=level.application,
        directory_roles=(role,) if role else (),
        resource=ResourceName.SharePoint,
    )
