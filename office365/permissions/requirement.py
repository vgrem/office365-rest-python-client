"""What a call needs from a tenant, spelled the same way by everyone who states it.

A live test states its precondition next to itself, a model method states the scopes its
request needs next to the request, and both are the same fact: *this call runs only if one of
these names is granted*. One dataclass keeps the two spellings from drifting, and lets the
skip message, the preflight report and the
:class:`~office365.runtime.exceptions.AccessDeniedException` hint render the same object.

Every group is an *any-of* and groups are combined with *and*: a requirement holds when the
tenant granted one name from each declared group. ``bypass_roles`` is the escape hatch -
holding one of them satisfies the whole requirement - which is how a directory role stands in
for a scope the app was never granted.

The names belong to one API resource (``Microsoft Graph``, ``Office 365 SharePoint Online``), so
a requirement carries it: ``Sites.ReadWrite.All`` is a different grant on each of the two, and a
requirement that dropped the resource would be checking one API's grants against another's.

This module is pure: it reads no tenant and sends no request. It checks a
:class:`TenantFacts` value, and the probe that reads one lives with the caller that owns a
client.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Iterable, Protocol

from office365.permissions.resource import ResourceName

if TYPE_CHECKING:
    from office365.permissions.declaration import PermissionRequirement

#: The ways a token can be obtained. A call runs under exactly one of them, so a requirement
#: names the names of at most one, and a declaration becomes one requirement per flow.
FLOWS = ("delegated", "application")


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

    ``delegated`` and ``application`` are alternatives of each other in general, but a single
    requirement names at most one of them, because a call runs under exactly one flow. A method
    that can be called either way states one requirement per flow.

    ``resource`` is the API the names mean something on, and it is one resource per requirement:
    names are not comparable across APIs, so a call that spans two APIs joins each separately.
    """

    delegated: tuple[str, ...] = ()
    application: tuple[str, ...] = ()
    roles: tuple[str, ...] = ()
    licenses: tuple[str, ...] = ()
    bypass_roles: tuple[str, ...] = ()
    resource: str = ResourceName.Graph

    @classmethod
    def join(
        cls,
        *declarations: PermissionRequirement,
        flow: str = "delegated",
        roles: Iterable[str] = (),
        licenses: Iterable[str] = (),
        bypass_roles: Iterable[str] = (),
    ) -> Requirement:
        """One requirement for several declarations, all read under the same ``flow``.

        A caller that exercises several endpoints - a live test, a migration job - needs what
        all of them need, so they are *conjoined*: names are merged into one group, and every
        extra group must be met as well. Within one declaration the names stay *alternatives*,
        which is how the method itself declared them.

        Declarations on different resources cannot be joined - the merged group would hold names
        that mean different things - so that is refused rather than answered with a union.

        The flow is stated by the caller, not inferred, because ``delegated`` and
        ``application`` are properties of the token a program runs under while a method usually
        declares both. Read what a call declares with
        :func:`~office365.permissions.declaration.declared`, which also rejects a declaration
        that says nothing about the flow in question.
        """
        if flow not in FLOWS:
            raise ValueError(f"flow must be one of {FLOWS}, not {flow!r}")
        if not declarations:
            raise ValueError("join needs at least one declaration")
        names: list[str] = []
        held: list[str] = list(roles)
        licensed: list[str] = list(licenses)
        bypass: list[str] = list(bypass_roles)
        for declaration in declarations:
            requirement = declaration.for_flow(flow)
            _extend(names, getattr(requirement, flow))
            _extend(held, requirement.roles)
            _extend(licensed, requirement.licenses)
            _extend(bypass, requirement.bypass_roles)
        shared = {
            "roles": tuple(held),
            "licenses": tuple(licensed),
            "bypass_roles": tuple(bypass),
            "resource": _shared_resource(declarations),
        }
        if flow == "application":
            return cls(application=tuple(names), **shared)
        return cls(delegated=tuple(names), **shared)

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
        parts = [f"{self.label(label)}: any of {', '.join(names)}" for label, names, _ in self.groups()]
        declared = " and ".join(parts)
        if self.bypass_roles:
            alternative = f"{self.label('role')}: any of {', '.join(self.bypass_roles)}"
            declared = f"{declared} or {alternative}" if declared else alternative
        return declared or "no declared permission"

    def label(self, group: str) -> str:
        """A group's label, naming the resource when it is not the default one."""
        return group if str(self.resource) == str(ResourceName.Graph) else f"{group} on {self.resource}"

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
        return [f"{self.label(label)}: any of {', '.join(names)}" for label, names in self.shortfall(state)]

    def satisfied_by(self, state: TenantFacts) -> bool:
        """Whether ``state`` meets this requirement."""
        return not self.unmet(state)


def _extend(target: list[str], values: Iterable[str]) -> None:
    """Append the names ``target`` does not hold yet, keeping declaration order."""
    target.extend(value for value in values if value not in target)


def _shared_resource(declarations: tuple[PermissionRequirement, ...]) -> str:
    """The one resource every declaration names, or a refusal to merge two APIs' names."""
    resources: list[str] = []
    _extend(resources, (str(declaration.resource) for declaration in declarations))
    if len(resources) > 1:
        raise ValueError(
            f"join needs declarations on one API resource, not {', '.join(resources)}: "
            "the same name is a different grant on each, so join each resource separately"
        )
    return declarations[0].resource if declarations else ResourceName.Graph
