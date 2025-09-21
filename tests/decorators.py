from functools import lru_cache, wraps
from typing import Any, Callable, List, TypeVar, cast
from unittest import TestCase

from office365.directory.applications.roles.collection import AppRoleCollection
from office365.directory.rolemanagement.role import DirectoryRole
from office365.entity_collection import EntityCollection
from office365.graph_client import GraphClient
from office365.runtime.types.collections import StringCollection
from tests import test_client_id

T = TypeVar("T", bound=Callable[..., Any])


@lru_cache(maxsize=1)
def _get_cached_permissions(client: GraphClient, client_id: str) -> AppRoleCollection:
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
                self.skipTest(
                    f"Required delegated permission '{', '.join(scopes)}' not granted"
                )

            return test_method(self, *args, **kwargs)

        return wrapper  # type: ignore[return-value]

    return decorator


@lru_cache(maxsize=1)
def _get_cached_directory_roles(client: GraphClient) -> EntityCollection[DirectoryRole]:
    """Get and cache application permissions for a client"""
    result = client.me.get_directory_roles().execute_query()
    return result


def requires_directory_role(*required_roles: str) -> Callable[[T], T]:
    """
    Decorator that checks if the user has at least one of the required directory roles.

    Args:
        *required_roles: One or more role names that are required to execute the function

    Returns:
        The decorated function if authorization succeeds, raises PermissionError otherwise
    """

    def decorator(func: T) -> T:
        @wraps(func)
        def wrapper(self: Any, *args: Any, **kwargs: Any) -> Any:
            client = getattr(self, "client", None)
            if not client:
                self.skipTest("No client available for directory roles check")

            # Get the user's current roles
            result = _get_cached_directory_roles(client)
            user_roles: List[str] = [role.display_name for role in result]

            # Check if user has at least one of the required roles
            has_required_role = any(role in user_roles for role in required_roles)

            if not has_required_role:
                required_roles_str = ", ".join(required_roles)
                user_roles_str = ", ".join(user_roles) if user_roles else "None"
                raise PermissionError(
                    f"Access denied. Requires one of these roles: {required_roles_str}. "
                    f"User has roles: {user_roles_str}"
                )

            return func(self, *args, **kwargs)

        return cast(T, wrapper)

    return decorator
