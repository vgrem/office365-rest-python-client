"""What a live test needs from the tenant: declared once, resolved one way.

A live test states its precondition next to itself — ``@requires_delegated("Mail.Read")``
— and this module is the only place that turns that statement into an answer. The
answer is a :class:`TenantState`: the facts about the signed-in app and user that the
check reads. It is gathered *selectively*, per requirement, because the facts are not
equally available to every token: an app-only client has no ``/me`` to ask for
licenses, and a delegated client may not be allowed to read its own grants. Asking for
a fact the flow cannot see would turn a skipped test into a failing one.

Because one object both *describes* a requirement and *checks* it, the runtime guard,
the skip message and the preflight report cannot disagree.

Nothing here sends a request except :meth:`TenantState.of`; everything else is pure.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from functools import lru_cache

from office365.directory.permissions.guard import (
    _cached_app_permissions,
    _cached_delegated_permissions,
    _cached_directory_roles,
)
from office365.graph_client import GraphClient
from office365.runtime.client_request_exception import ClientRequestException


@lru_cache(maxsize=1)
def _cached_licenses(client: GraphClient) -> tuple[str, ...]:
    """The signed-in user's license SKU part numbers (a delegated-token fact only)."""
    details = client.me.license_details.get().execute_query()
    return tuple(detail.get_property("skuPartNumber") for detail in details)


@dataclass(frozen=True)
class TenantState:
    """The tenant facts a requirement reads; empty sets mean "not asked for"."""

    delegated: frozenset[str] = frozenset()
    application: frozenset[str] = frozenset()
    roles: frozenset[str] = frozenset()
    licenses: frozenset[str] = frozenset()
    #: Why the facts could not be read at all (a refused permission lookup).
    unverifiable: str = ""

    @classmethod
    def of(cls, client: GraphClient, client_id: str, requirement: Requirement) -> TenantState:
        """Read exactly the facts ``requirement`` names, or say why they could not be read."""
        delegated: frozenset[str] = frozenset()
        application: frozenset[str] = frozenset()
        roles: frozenset[str] = frozenset()
        licenses: frozenset[str] = frozenset()
        try:
            if requirement.delegated:
                delegated = frozenset(_cached_delegated_permissions(client, client_id))
            if requirement.application:
                application = frozenset(role.value for role in _cached_app_permissions(client, client_id))
            if requirement.roles or requirement.bypass_roles:
                roles = frozenset(role.display_name for role in _cached_directory_roles(client))
            if requirement.licenses:
                licenses = frozenset(_cached_licenses(client))
        except ClientRequestException:
            return cls(unverifiable="the permission lookup needs a scope this token does not have")
        return cls(delegated=delegated, application=application, roles=roles, licenses=licenses)


@dataclass(frozen=True)
class Requirement:
    """A test's precondition, as the decorators accept it.

    Every group is an *any-of*; groups are combined with *and* (a test needs the scope
    it names and the role it names and the license it names). ``bypass_roles`` is the
    escape hatch: holding one of them satisfies the whole requirement.
    """

    delegated: tuple[str, ...] = ()
    application: tuple[str, ...] = ()
    roles: tuple[str, ...] = ()
    licenses: tuple[str, ...] = ()
    bypass_roles: tuple[str, ...] = ()

    def groups(self) -> list[tuple[str, tuple[str, ...], str]]:
        """(label, names, state field) for every declared group, in report order."""
        declared = (
            ("delegated", self.delegated, "delegated"),
            ("application", self.application, "application"),
            ("directory role", self.roles, "roles"),
            ("license", self.licenses, "licenses"),
        )
        return [(label, names, attribute) for label, names, attribute in declared if names]

    def describe(self) -> str:
        """A one-line statement of what the test needs, for a report or a skip message."""
        parts = [f"{label}: any of {', '.join(names)}" for label, names, _ in self.groups()]
        declared = " and ".join(parts)
        if self.bypass_roles:
            alternative = f"role: any of {', '.join(self.bypass_roles)}"
            declared = f"{declared} or {alternative}" if declared else alternative
        return declared or "no declared permission"

    def unmet(self, state: TenantState) -> list[str]:
        """The declared groups ``state`` does not satisfy — empty when the test may run."""
        if state.unverifiable:
            return [state.unverifiable]
        if self.bypass_roles and set(self.bypass_roles) & state.roles:
            return []
        return [
            f"{label}: any of {', '.join(names)}"
            for label, names, attribute in self.groups()
            if not set(names) & getattr(state, attribute)
        ]

    def satisfied_by(self, state: TenantState) -> bool:
        """Whether ``state`` meets this requirement."""
        return not self.unmet(state)


@dataclass
class Needs:
    """Every requirement one suite declares, with the tests that declare it."""

    suite: str
    flow: str
    tests: int = 0
    requirements: dict[Requirement, list[str]] = field(default_factory=dict)

    def add(self, requirement: Requirement, test_name: str) -> None:
        """Record that ``test_name`` declares ``requirement``."""
        self.requirements.setdefault(requirement, []).append(test_name)

    def unmet_for(self, states: dict[Requirement, TenantState]) -> list[tuple[Requirement, list[str]]]:
        """The requirements these resolved states do not satisfy, with the tests they block.

        A requirement with no resolved state is *not* reported: "not verified" is
        different from "missing", and confusing the two is how a report stops being read.
        """
        return [
            (requirement, tests)
            for requirement, tests in self.requirements.items()
            if (state := states.get(requirement)) is not None and not requirement.satisfied_by(state)
        ]


def declared_requirement(test_method: object) -> Requirement | None:
    """The requirement a decorated test declares, if any — read, never called.

    The decorators stamp the object they return, so the matrix is introspected from
    the tests themselves rather than from a list kept beside them.
    """
    requirement = getattr(test_method, "__requires__", None)
    return requirement if isinstance(requirement, Requirement) else None
