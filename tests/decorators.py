"""Skip a live test when the tenant does not meet the precondition it declares."""

from __future__ import annotations

from functools import wraps
from typing import Any, Callable, TypeVar, cast
from unittest import TestCase

from office365.permissions import Requirement, ResourceName, declared

from tests import test_client_id
from tests.capabilities import TenantState

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


def requires_application(*app_roles: str, resource: str = ResourceName.Graph) -> Callable[[T], T]:
    """Skip the test unless the app holds one of these application permissions on ``resource``."""
    return _requires(Requirement(application=tuple(app_roles), resource=resource))


def requires_call(
    *calls: Callable[..., Any],
    flow: str = "delegated",
    bypass_roles: list[str] | None = None,
    require_roles: list[str] | None = None,
    require_licenses: list[str] | None = None,
) -> Callable[[T], T]:
    """Skip the test unless the tenant grants what the model methods it calls declare.

    The requirement is derived, not restated: each call carries its ``@require_permission``
    declaration beside the request it builds, and the library's
    :meth:`~office365.permissions.requirement.Requirement.join` turns them into one requirement.
    A test that sends and then reads needs both, and the extras a declaration cannot know (a
    bypass role, an SKU) are added here.

    Args:
        *calls: The model methods the test exercises, e.g. ``Message.send`` — the
            unbound class attribute, so the declaration is *read*, never called.
        flow: Which declaration column the test runs under: ``"delegated"`` for a signed-in
            user, ``"application"`` for an app-only client. A method that declares nothing
            under this flow raises here rather than skipping for ever.
        bypass_roles: Directory roles - holding one satisfies the whole requirement.
        require_roles: Directory roles - one must be held.
        require_licenses: SKU part numbers (e.g. ``SPE_E5``) - one must be held.

    The API resource is derived too, from the declarations: a test may not join a Graph call
    to a SharePoint one, because the same name is a different grant on each.
    """
    return _requires(
        Requirement.join(
            *(declared(call, flow=flow) for call in calls),
            flow=flow,
            roles=require_roles or (),
            licenses=require_licenses or (),
            bypass_roles=bypass_roles or (),
        )
    )


def requires_delegated(
    *scopes: str,
    bypass_roles: list[str] | None = None,
    require_roles: list[str] | None = None,
    require_licenses: list[str] | None = None,
    resource: str = ResourceName.Graph,
) -> Callable[[T], T]:
    """Skip the test unless it has a declared scope *and* every declared role/license.

    Args:
        *scopes: Delegated (or application) permission names — any one suffices.
        bypass_roles: Directory roles — holding one satisfies the whole requirement.
        require_roles: Directory roles — one must be held.
        require_licenses: SKU part numbers (e.g. ``SPE_E5``) — one must be held.
        resource: The API the scopes belong to, e.g. ``ResourceName.SharePoint``; a scope name
            is only granted, and only checkable, within the API that defines it.
    """
    return _requires(
        Requirement(
            delegated=tuple(scopes),
            roles=tuple(require_roles or ()),
            licenses=tuple(require_licenses or ()),
            bypass_roles=tuple(bypass_roles or ()),
            resource=resource,
        )
    )
