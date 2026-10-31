"""What an API call needs from a tenant, spelled the same way by everyone who states it.

A live test states its precondition next to itself, a model method states the scopes its
request needs next to the request, and both are the same fact: *this call runs only if
one of these names is granted*. One dataclass keeps the two spellings from drifting, and
lets the skip message, the preflight report and the
:class:`~office365.runtime.exceptions.AccessDeniedException` hint render the same object.

Every group is an *any-of* and groups are combined with *and*: a requirement holds when
the tenant granted one name from each declared group. ``bypass_roles`` is the escape
hatch - holding one of them satisfies the whole requirement - which is how a directory
role stands in for a scope the app was never granted.

This module is pure: it reads no tenant and sends no request. It checks a
:class:`TenantFacts` value, and the probe that reads one lives with the caller that owns
a client.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


class TenantFacts(Protocol):
    """The tenant facts a requirement reads. Empty means "not asked for", not "not granted"."""

    @property
    def delegated(self) -> frozenset[str]: ...

    @property
    def application(self) -> frozenset[str]: ...

    @property
    def roles(self) -> frozenset[str]: ...

    @property
    def licenses(self) -> frozenset[str]: ...

    @property
    def unverifiable(self) -> str:
        """Why the facts could not be read at all (a refused permission lookup)."""
        ...


@dataclass(frozen=True)
class Requirement:
    """A precondition of a call, as the decorators accept it.

    ``delegated`` and ``application`` are alternatives of each other in general, but a
    single requirement names at most one of them, because a call runs under exactly one
    flow. A method that can be called either way states one requirement per flow.
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
        """A one-line statement of what the call needs, for a report or a skip message."""
        parts = [f"{label}: any of {', '.join(names)}" for label, names, _ in self.groups()]
        declared = " and ".join(parts)
        if self.bypass_roles:
            alternative = f"role: any of {', '.join(self.bypass_roles)}"
            declared = f"{declared} or {alternative}" if declared else alternative
        return declared or "no declared permission"

    def shortfall(self, state: TenantFacts) -> list[tuple[str, tuple[str, ...]]]:
        """The declared groups ``state`` leaves unmet, as (label, names) - empty when it may run."""
        if state.unverifiable or (self.bypass_roles and set(self.bypass_roles) & state.roles):
            return []
        return [
            (label, names) for label, names, attribute in self.groups() if not set(names) & getattr(state, attribute)
        ]

    def unmet(self, state: TenantFacts) -> list[str]:
        """The declared groups ``state`` does not satisfy - empty when the call may run."""
        if state.unverifiable:
            return [state.unverifiable]
        return [f"{label}: any of {', '.join(names)}" for label, names in self.shortfall(state)]

    def satisfied_by(self, state: TenantFacts) -> bool:
        """Whether ``state`` meets this requirement."""
        return not self.unmet(state)
