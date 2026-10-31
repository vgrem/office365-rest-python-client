"""Skip a live test when the tenant does not meet the precondition it declares."""

from __future__ import annotations

from functools import wraps
from typing import Any, Callable, TypeVar, cast
from unittest import TestCase

from tests import test_client_id
from tests.capabilities import Requirement, TenantState

T = TypeVar("T", bound=Callable[..., Any])


def _requires(requirement: Requirement) -> Callable[[T], T]:
    """Build the decorator that stamps ``requirement`` and enforces it.

    The stamp is the point: :mod:`tests.preflight` reads it off the test tree to
    report what a tenant must grant before the test can run, without running it.
    """

    def decorator(test_method: T) -> T:
        @wraps(test_method)
        def wrapper(self: TestCase, *args: Any, **kwargs: Any) -> Any:
            client = getattr(self, "client", None)
            if client is None:
                self.skipTest("no client to check permissions against")
            unmet = requirement.unmet(TenantState.of(client, test_client_id, requirement))
            if unmet:
                self.skipTest(f"missing {' and '.join(unmet)}")
            return test_method(self, *args, **kwargs)

        wrapper.__requires__ = requirement
        return cast(T, wrapper)

    return decorator


def requires_application(*app_roles: str) -> Callable[[T], T]:
    """Skip the test unless the app holds one of these application permissions."""
    return _requires(Requirement(application=tuple(app_roles)))


def requires_delegated(
    *scopes: str,
    bypass_roles: list[str] | None = None,
    require_roles: list[str] | None = None,
    require_licenses: list[str] | None = None,
) -> Callable[[T], T]:
    """Skip the test unless it has a declared scope *and* every declared role/license.

    Args:
        *scopes: Delegated (or application) permission names — any one suffices.
        bypass_roles: Directory roles — holding one satisfies the whole requirement.
        require_roles: Directory roles — one must be held.
        require_licenses: SKU part numbers (e.g. ``SPE_E5``) — one must be held.
    """
    return _requires(
        Requirement(
            delegated=tuple(scopes),
            roles=tuple(require_roles or ()),
            licenses=tuple(require_licenses or ()),
            bypass_roles=tuple(bypass_roles or ()),
        )
    )
