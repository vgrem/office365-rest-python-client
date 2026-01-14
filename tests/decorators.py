from functools import lru_cache, wraps
from typing import Any, Callable, TypeVar
from unittest import TestCase

from office365.directory.applications.roles.collection import AppRoleCollection
from office365.graph_client import GraphClient
from office365.runtime.types.collections import StringCollection
from tests import test_client_id

T = TypeVar("T", bound=Callable[..., Any])


@lru_cache(maxsize=1)
def _get_cached_permissions(client, client_id):
    # type: (GraphClient, str) -> AppRoleCollection
    """Get and cache application permissions for a client"""
    resource = client.service_principals.get_by_name("Microsoft Graph")
    result = resource.get_application_permissions(client_id).execute_query()
    return result.value


def requires_app_permission(*app_roles):
    # type: (*str) -> Callable[[T], T]
    def decorator(test_method):
        # type: (T) -> T
        @wraps(test_method)
        def wrapper(self, *args, **kwargs):
            # type: (TestCase, *Any, **Any) -> Any
            client = getattr(self, "client", None)
            if not client:
                self.skipTest("No client available for permission check")

            permissions = _get_cached_permissions(client, test_client_id)

            if not any(role.value in app_roles for role in permissions):
                required_roles = ", ".join(f"'{role}'" for role in app_roles)
                self.skipTest(f"Required app permission '{required_roles}' not granted")

            return test_method(self, *args, **kwargs)

        return wrapper

    return decorator


@lru_cache(maxsize=1)
def _get_cached_delegated_permissions(client, client_id):
    # type: (GraphClient, str) -> StringCollection
    """Get and cache delegated permissions for a client"""
    resource = client.service_principals.get_by_name("Microsoft Graph")
    result = resource.get_delegated_permissions(client_id).execute_query()
    return result.value


def requires_delegated_permission(*scopes):
    # type: (*str) -> Callable[[T], T]
    """Decorator to verify delegated permissions before test execution"""

    def decorator(test_method):
        # type: (T) -> T
        @wraps(test_method)
        def wrapper(self, *args, **kwargs):
            # type: (TestCase, *Any, **Any) -> Any
            client = getattr(self, "client", None)
            if not client:
                self.skipTest("No client available for permission check")

            # Get permissions from cache or API
            granted_scopes = _get_cached_delegated_permissions(client, test_client_id)

            if not any(scope in granted_scopes for scope in scopes):
                self.skipTest(f"Required delegated permission '{', '.join(scopes)}' not granted")

            return test_method(self, *args, **kwargs)

        return wrapper  # type: ignore[return-value]

    return decorator
