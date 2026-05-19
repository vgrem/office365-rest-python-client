"""Test decorators for permission and role checks."""

from __future__ import annotations

from functools import wraps
from typing import Any, Callable, TypeVar, cast
from unittest import TestCase

from office365.directory.permissions.guard import (
    _cached_app_permissions,
    _cached_delegated_permissions,
    has_app_permission,
    has_delegated_permission,
    has_role,
)

from tests import test_client_id

T = TypeVar("T", bound=Callable[..., Any])


def requires_app_permission(*app_roles: str) -> Callable[[T], T]:
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
    or_roles: list[str] | None = None,
) -> Callable[[T], T]:
    """Skip test unless token has one of the scopes (delegated or app)
    OR the user has one of the directory roles.

    Args:
        *scopes: Delegated or application permission names — ANY match passes.
        or_roles: Directory role display names — ANY match passes (fallback).
    """

    def decorator(test_method: T) -> T:
        @wraps(test_method)
        def wrapper(self: TestCase, *args: Any, **kwargs: Any) -> Any:
            client = getattr(self, "client", None)
            if not client:
                self.skipTest("No client available")

            has_scope = any(
                has_delegated_permission(client, s, test_client_id)
                or has_app_permission(client, s, test_client_id)
                for s in scopes
            )
            has_dir_role = any(has_role(client, r) for r in (or_roles or []))

            if has_scope or has_dir_role:
                return test_method(self, *args, **kwargs)

            reasons = []
            if scopes:
                reasons.append(f"one of scopes: {', '.join(scopes)}")
            if or_roles:
                reasons.append(f"one of roles: {', '.join(or_roles)}")
            self.skipTest(f"Insufficient permissions — required: {' or '.join(reasons)}")

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
