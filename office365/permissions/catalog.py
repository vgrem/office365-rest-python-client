"""What an API publishes, so a name can be checked where it is written.

A declaration says what a call needs; this says what the API *offers*. The two are different
facts and neither implies the other, which is why a wrong permission name survives every live
test: the request is refused, the suite skips, and the refusal reads like a missing grant.
Reading the API's own service principal - ``appRoles`` for application permissions,
``oauth2PermissionScopes`` for delegated ones - turns the name into something a test can check
while nobody is signed in.

The snapshots under :mod:`office365.permissions.snapshots` are **generated** from the tenant by
``scripts/gen_permission_catalog.py`` and committed, so the check is offline; a live test
compares them with the tenant again, so a snapshot that goes stale is a red test rather than a
stale answer. Nothing here sends a request and nothing here holds a client: a :class:`Catalog`
is data.

Names, not prose: the description Microsoft ships with a permission is edited freely and would
make the ratchet noisy, so only the facts that decide whether a grant is possible - published,
enabled, and whether a user may consent - are recorded.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from typing import FrozenSet, List, Optional

from office365.permissions.requirement import FLOWS
from office365.permissions.snapshots import graph, sharepoint

#: A signed-in user can carry it, when the API lets a user consent to it.
#: An administrator grants an :data:`APPLICATION` permission on behalf of the whole tenant.
DELEGATED, APPLICATION = FLOWS

#: The committed snapshots, keyed by the display name a declaration names. A ``ResourceName``
#: member hashes by its name rather than its value, so every lookup goes through ``str``.
_SOURCES = {str(module.RESOURCE): module for module in (graph, sharepoint)}


@dataclass(frozen=True)
class Catalog:
    """The permissions one API publishes, split by the flow that asks for them.

    Args:
        resource: The API's display name, as :class:`~office365.permissions.resource.ResourceName`
            spells it - the same value a declaration names.
        delegated: Names published as ``oauth2PermissionScopes``.
        application: Names published as ``appRoles``.
        user_consentable: Delegated names a signed-in user may consent to; the rest of them,
            like every application permission, need an administrator.
        disabled: Names still published but switched off, so no grant of them is possible.
    """

    resource: str
    delegated: FrozenSet[str] = frozenset()
    application: FrozenSet[str] = frozenset()
    user_consentable: FrozenSet[str] = frozenset()
    disabled: FrozenSet[str] = frozenset()

    def names(self, kind: str = DELEGATED) -> FrozenSet[str]:
        """The names published for ``kind``, whatever their state."""
        _check_kind(kind)
        return self.delegated if kind == DELEGATED else self.application

    def publishes(self, name: str, kind: str = DELEGATED) -> bool:
        """Whether ``name`` is a permission this API publishes *and* can still grant."""
        return name in self.names(kind) and name not in self.disabled

    def requires_admin_consent(self, name: str, kind: str = DELEGATED) -> bool:
        """Whether only an administrator can grant ``name``, rather than a signed-in user."""
        _check_kind(kind)
        return kind == APPLICATION or name not in self.user_consentable


@lru_cache(maxsize=None)
def catalog(resource: str) -> Optional[Catalog]:
    """The published permissions of ``resource``, or ``None`` when it has no snapshot yet."""
    source = _SOURCES.get(str(resource))
    if source is None:
        return None
    return Catalog(
        resource=source.RESOURCE,
        application=frozenset(source.APPLICATION.split()),
        delegated=frozenset(source.DELEGATED.split()),
        user_consentable=frozenset(source.USER_CONSENTABLE.split()),
        disabled=frozenset(source.DISABLED.split()),
    )


def catalog_resources() -> List[str]:
    """The APIs that have a snapshot - what :func:`catalog` answers to."""
    return list(_SOURCES)


def _check_kind(kind: str) -> None:
    if kind not in FLOWS:
        raise ValueError(f"kind must be one of {FLOWS}, not {kind!r}")
