"""Test decorators for permission and role checks."""

from __future__ import annotations

from functools import wraps
from typing import Any, Callable, TypeVar, cast
from unittest import TestCase

from office365.directory.permissions.guard import (
    _cached_delegated_permissions,
    has_app_permission,
    has_delegated_permission,
    has_role,
)

from tests import test_client_id

T = TypeVar("T", bound=Callable[..., Any])


def requires_delegated_permission_or_role(
    *scopes: str,
    roles: list[str] | None = None,
) -> Callable[[T], T]:
    """Skip test unless app has permission OR user has directory role.

    Checks delegated permissions, then application permissions,
    then directory roles. Test runs if ANY check passes.

    Args:
        *scopes: Permission names to check (delegated or app-only)
        roles: Directory role names to check
    """

    def decorator(test_method: T) -> T:
        @wraps(test_method)
        def wrapper(self: TestCase, *args: Any, **kwargs: Any) -> Any:
            client = getattr(self, "client", None)
            if not client:
                self.skipTest("No client available")

            if scopes:
                for scope in scopes:
                    if has_delegated_permission(client, scope, test_client_id) or has_app_permission(
                        client, scope, test_client_id
                    ):
                        return test_method(self, *args, **kwargs)

            if roles:
                for role in roles:
                    if has_role(client, role):
                        return test_method(self, *args, **kwargs)

            reasons = []
            if scopes:
                reasons.append(f"scope {', '.join(scopes)}")
            if roles:
                reasons.append(f"role {', '.join(roles)}")
            self.skipTest(f"Missing {' nor '.join(reasons)}")

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
