"""What an API publishes, so a name can be checked where it is written.

A declaration says what a call needs; this says what the API *offers*. The two are different
facts and neither implies the other, which is why a wrong permission name survives every live
test: the request is refused, the suite skips, and the refusal reads like a missing grant.

A service principal publishes its own vocabulary - ``appRoles`` for application permissions,
``oauth2PermissionScopes`` for delegated ones - so the answer is read from the tenant that owns
the API, never copied next to the declarations. A copy answers for the day it was taken: three
weeks after the one this replaced was generated, the same tenant published ten more delegated
names and twelve more app roles than the copy held, and nothing had failed.

Nothing here sends a request and nothing here holds a client: a :class:`Catalog` is data, and
:meth:`Catalog.of` builds one from a principal the caller has already read.

Names, not prose: the description Microsoft ships with a permission is edited freely, so only
the lists that decide a grant are kept.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, FrozenSet, Iterable

from office365.permissions.requirement import FLOWS

#: A signed-in user can carry it, when the API lets a user consent to it.
#: An administrator grants an :data:`APPLICATION` permission on behalf of the whole tenant.
DELEGATED, APPLICATION = FLOWS


@dataclass(frozen=True)
class Catalog:
    """The permissions one API publishes, split by the flow that asks for them.

    Args:
        delegated: Names published as ``oauth2PermissionScopes``.
        application: Names published as ``appRoles``.
    """

    delegated: FrozenSet[str] = frozenset()
    application: FrozenSet[str] = frozenset()

    @classmethod
    def of(cls, principal: Any) -> Catalog:
        """The catalog a read ``servicePrincipal`` publishes.

        Args:
            principal: The API's own principal, read with ``appRoles`` and
                ``oauth2PermissionScopes`` selected - see
                :func:`~office365.directory.permissions.guard.published_permissions`.

        A name the API still lists but has switched off is not published in the sense that
        matters here: no grant of it can be minted, so a declaration that names one is wrong in
        the same way a misspelling is.
        """
        return cls(
            application=frozenset(_values(principal.app_roles)),
            delegated=frozenset(_values(principal.oauth2_permission_scopes)),
        )

    def names(self, kind: str = DELEGATED) -> FrozenSet[str]:
        """The names published for ``kind``."""
        _check_kind(kind)
        return self.delegated if kind == DELEGATED else self.application

    def publishes(self, name: str, kind: str = DELEGATED) -> bool:
        """Whether ``name`` is a permission this API publishes and can still grant."""
        return name in self.names(kind)


def _values(rows: Iterable[Any]) -> list[str]:
    """The grantable names of ``rows``: a permission appears once per member type, and a
    switched-off one is listed by the API without being grantable."""
    return [row.value for row in rows or () if row.value and getattr(row, "isEnabled", True) is not False]


def _check_kind(kind: str) -> None:
    if kind not in FLOWS:
        raise ValueError(f"kind must be one of {FLOWS}, not {kind!r}")
