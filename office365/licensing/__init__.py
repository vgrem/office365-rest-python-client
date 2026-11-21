"""Whether a tenant can make a call at all, as distinct from whether it is allowed to.

A permission can be granted to anyone who asks for it; a licence is bought, and no grant
creates one. ``office365.permissions`` therefore answers *who may* - a scope, a directory
role, a declaration - while this package answers *whether the capability exists in this
tenant*, which is the question a 403 on an unlicensed tenant fails to answer.

:class:`~office365.licensing.guard.LicenceGuard` reads the markers declared with
:func:`~office365.permissions.declaration.requires_license`. It is given one thing: how to
learn what the tenant holds. It never holds a client, and nothing here talks to a request.

The guard is off unless a caller turns it on (``O365_LICENCE_GUARD=warn`` or ``=enforce``),
because a check that costs a request of its own must be asked for rather than assumed, and a
library that reads subscriptions on import would surprise every script.

Nothing here carries a product catalogue: what a tenant holds comes from its own
``subscribedSkus``, and which retail SKU would add a plan is Microsoft's published data, not
something Graph returns.
"""

from office365.licensing.guard import ENFORCE, ENVIRONMENT, MODES, OFF, WARN, LicenceGuard, LicenceRequired

__all__ = [
    "ENFORCE",
    "ENVIRONMENT",
    "MODES",
    "OFF",
    "WARN",
    "LicenceGuard",
    "LicenceRequired",
]

#: A check on what a tenant bought, not a product of its own.
__product__ = ""
