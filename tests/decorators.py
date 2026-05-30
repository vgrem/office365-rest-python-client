"""Test decorators for permission and role checks."""

from __future__ import annotations

from functools import wraps
from typing import Any, Callable, TypeVar, cast
from unittest import TestCase

from functools import lru_cache

from office365.directory.permissions.guard import (
    _cached_app_permissions,
    _cached_delegated_permissions,
    has_delegated_permission,
    has_role,
)
from office365.graph_client import GraphClient

from tests import test_client_id

T = TypeVar("T", bound=Callable[..., Any])


@lru_cache(maxsize=1)
def _cached_licenses(client: GraphClient) -> list[str]:
    """Get and cache the signed-in user's license SKU part numbers."""
    result = client.me.license_details.get().execute_query()
    return [d.get_property("skuPartNumber") for d in result]


def requires_application(*app_roles: str) -> Callable[[T], T]:
    """Skip test unless the app has the required application permissions."""

    def decorator(test_method: T) -> T:
        @wraps(test_method)
        def wrapper(self: TestCase, *args: Any, **kwargs: Any) -> Any:
            client = getattr(self, "client", None)
            if not client:
                self.skipTest("No client available for permission check")

            permissions = _cached_app_permissions(client, test_client_id)

            if not any(role.value in app_roles for role in permissions):
                required = ", ".join(f"'{r}'" for r in app_roles)
                self.skipTest(f"Required app permission {required} not granted")

            return test_method(self, *args, **kwargs)

        return cast(T, wrapper)

    return decorator


def requires_delegated(
    *scopes: str,
    bypass_roles: list[str] | None = None,
    require_roles: list[str] | None = None,
    require_licenses: list[str] | None = None,
) -> Callable[[T], T]:
    """Skip test unless token has one of the scopes (delegated or app)
    AND the user has all required require_roles,
    OR the user has one of the bypass_roles (bypass).

    Args:
        *scopes: Delegated or application permission names — ANY match passes.
        bypass_roles: Directory role display names — ANY match bypasses all checks.
        require_roles: Directory role display names — ANY must match (OR with scopes).
        require_licenses: SKU part numbers — ANY must match (e.g. SPE_E5).
    """

    def decorator(test_method: T) -> T:
        @wraps(test_method)
        def wrapper(self: TestCase, *args: Any, **kwargs: Any) -> Any:
            client = getattr(self, "client", None)
            if not client:
                self.skipTest("No client available")
            assert client is not None

            has_scope = any(has_delegated_permission(client, s, test_client_id) for s in scopes)
            has_require = not require_roles or any(has_role(client, r) for r in require_roles)
            has_bypass = any(has_role(client, r) for r in (bypass_roles or []))
            has_license = not require_licenses or any(
                lic in _cached_licenses(client) for lic in require_licenses
            )

            if has_bypass or (has_scope and has_require and has_license):
                return test_method(self, *args, **kwargs)

            reasons = []
            if scopes:
                reasons.append(f"one of scopes: {', '.join(scopes)}")
            if require_roles:
                reasons.append(f"one of roles: {', '.join(require_roles)}")
            if require_licenses:
                reasons.append(f"one of licenses: {', '.join(require_licenses)}")
            if bypass_roles:
                reasons.append(f"one of bypass roles: {', '.join(bypass_roles)}")
            self.skipTest(f"Insufficient — required: {' and '.join(reasons)}")

        return cast(T, wrapper)

    return decorator


def requires_delegated_permission(*scopes: str) -> Callable[[T], T]:
    """Skip test unless the app has the required delegated permissions."""

    def decorator(test_method: T) -> T:
        @wraps(test_method)
        def wrapper(self: TestCase, *args: Any, **kwargs: Any) -> Any:
            client = getattr(self, "client", None)
            if not client:
                self.skipTest("No client available for permission check")

            granted = _cached_delegated_permissions(client, test_client_id)

            if not any(scope in granted for scope in scopes):
                self.skipTest(f"Required delegated permission '{', '.join(scopes)}' not granted")

            return test_method(self, *args, **kwargs)

        return cast(T, wrapper)

    return decorator
