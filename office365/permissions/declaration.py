"""What a model method's request needs, stated beside the request it builds.

``@require_permission(delegated=[...], application=[...])`` marks the method, and the mark is
the only thing anyone reads: a live test derives its precondition from it, the runtime names
it when a request is denied, and a report lists it beside the endpoint. A wrapper around
another declared method borrows its mark with ``@derived_from`` instead of restating it.
Nothing calls the method to learn what it needs, so the declaration cannot drift from the code
by being wrong at the wrong time - it is either there or it is not.

The decorator does three things, one helper each:

:func:`_stamp`
    attach the declaration to the function (read it back with :func:`declared`);
:func:`_tag_query`
    tag the query this call queues, so a denial can name what the request needed;
:func:`_document`
    append the declared names to the docstring, so ``help()`` shows them.

None of them sends a request, and none of them can: the tagged query belongs to the caller's
context, and the tag is a local attribute write on a query that is already built.
"""

from __future__ import annotations

import inspect
import textwrap
from collections.abc import Iterable
from dataclasses import dataclass
from functools import wraps
from typing import Any, Callable, TypeVar, cast

from typing_extensions import ParamSpec

from office365.permissions.requirement import FLOWS, Requirement
from office365.permissions.resource import ResourceName

P = ParamSpec("P")
F = TypeVar("F", bound=Callable[..., Any])

#: Where the declaration is visible on a decorated method. Read it with :func:`declared`,
#: which explains what a missing one means.
STAMP = "__required_permissions__"


@dataclass(frozen=True)
class PermissionRequirement:
    """The permissions a request needs, as the official Graph documentation table states them.

    The Graph REST reference lists a *Delegated* and an *Application* column for every
    endpoint; those become :attr:`delegated` and :attr:`application`. A directory role that may
    also make the call is a *bypass* for whoever holds it - holding it satisfies the whole
    requirement rather than adding one more group to meet - which is what
    :attr:`directory_roles` means.

    :attr:`resource` is the API the names belong to. It is not decoration: ``Sites.ReadWrite.All``
    and ``Mail.Send`` each exist on more than one API, granted separately, unlocking different
    endpoints - so a request that names a permission without naming its API cannot be checked
    against the right grants, and would be checked against Microsoft Graph's by default.

    Frozen on purpose: a declaration is read from many places (a test, a report, a denial) and
    a mutable one would let one reader edit what the next one sees.
    """

    delegated: tuple[str, ...] = ()
    application: tuple[str, ...] = ()
    directory_roles: tuple[str, ...] = ()
    licenses: tuple[str, ...] = ()
    notes: str = ""
    resource: str = ResourceName.Graph

    def for_flow(self, flow: str) -> Requirement:
        """This declaration as the single requirement a call under ``flow`` must meet.

        A projection, not a validation: a declaration that says nothing about ``flow``
        projects to a requirement with no names, and :func:`declared` is where that becomes an
        error, because only it knows the name of the method to blame.
        """
        if flow not in FLOWS:
            raise ValueError(f"flow must be one of {FLOWS}, not {flow!r}")
        return Requirement(
            **{flow: getattr(self, flow)},
            licenses=self.licenses,
            bypass_roles=self.directory_roles,
            resource=self.resource,
        )

    def requirements(self) -> tuple[Requirement, ...]:
        """One :class:`Requirement` per flow this method can run under.

        The two flows are alternatives for the caller rather than conjuncts, so they become two
        requirements instead of one. A declaration that names only a bypass role still states
        something checkable, so it yields the role-only requirement instead of nothing.
        """
        flows = tuple(requirement for requirement in (self.for_flow(flow) for flow in FLOWS) if requirement.groups())
        if flows or not self.directory_roles:
            return flows
        return (Requirement(licenses=self.licenses, bypass_roles=self.directory_roles, resource=self.resource),)

    def to_hint(self) -> str:
        """One-line remediation naming the declared permissions (may be empty).

        Shown by an :class:`~office365.runtime.exceptions.AccessDeniedException` when a
        decorated method's request is rejected.
        """
        scopes: list[str] = []
        if self.application:
            scopes.append(f"application {', '.join(self.application)}")
        if self.delegated:
            scopes.append(f"delegated {', '.join(self.delegated)}")
        if self.directory_roles:
            scopes.append(f"directory role {', '.join(self.directory_roles)}")
        if not scopes:
            return ""
        where = "" if str(self.resource) == str(ResourceName.Graph) else f" (on {self.resource})"
        hint = f"This API declares{where}: " + "; ".join(scopes) + "."
        if self.notes:
            hint += f" ({self.notes})"
        return hint

    def describe(self) -> str:
        """The declaration as the lines a docstring shows, one line per declared column."""
        columns = (
            ("Delegated", self.delegated),
            ("Application", self.application),
            ("Directory roles", self.directory_roles),
            ("Licenses", self.licenses),
        )
        resource = [] if str(self.resource) == str(ResourceName.Graph) else [f"Resource: {self.resource}"]
        lines = resource + [f"{label}: {', '.join(names)}" for label, names in columns if names]
        if self.notes:
            lines.append(f"Notes: {self.notes}")
        return "\n".join(lines)


def declared(func: Callable[..., Any], flow: str | None = None) -> PermissionRequirement:
    """The declaration stamped on ``func``, or a loud failure naming it.

    This is the only way to read a declaration, and it refuses two kinds of silence: a method
    that names no permission at all, and one that names nothing under the ``flow`` the caller
    runs under. Both would otherwise produce an empty requirement - a check that always
    passes, which is the failure mode worth more than the two exceptions.
    """
    declaration = getattr(func, STAMP, None)
    if not isinstance(declaration, PermissionRequirement):
        raise ValueError(
            f"{_name(func)} names no permission: decorate the method with @require_permission, "
            "or the requirement derived from it would be empty"
        )
    if flow is not None and not getattr(declaration.for_flow(flow), flow):
        raise ValueError(
            f"{_name(func)} declares no {flow} permission: pass flow='application', or declare its {flow} column"
        )
    return declaration


def require_permission(
    delegated: Iterable[str] | None = None,
    application: Iterable[str] | None = None,
    directory_roles: Iterable[str] | None = None,
    licenses: Iterable[str] | None = None,
    notes: str = "",
    resource: str = ResourceName.Graph,
) -> Callable[[F], F]:
    """Declare the permissions the decorated method's request needs.

    Args:
        delegated: Scope names for a signed-in user, e.g. ``["Mail.Send"]``.
        application: App-only permission names for the same call.
        directory_roles: Entra ID roles - holding one satisfies the whole call.
        licenses: SKU part numbers - one must be held.
        notes: Free text for anything the columns cannot say.
        resource: The API the names belong to, e.g. ``ResourceName.SharePoint`` for the
            endpoints under :mod:`office365.sharepoint`. Defaults to Microsoft Graph; the names
            are only meaningful - and only checkable - against the API that defines them.

    The declaration is stamped as ``method.__required_permissions__``, tagged onto the query
    the method queues (so a denial names it) and appended to the docstring (so ``help(method)``
    shows it). None of that costs a request or an import: three attribute reads and one write
    per call.
    """
    declaration = PermissionRequirement(
        delegated=tuple(delegated or ()),
        application=tuple(application or ()),
        directory_roles=tuple(directory_roles or ()),
        licenses=tuple(licenses or ()),
        notes=notes,
        resource=resource,
    )

    def decorate(func: F) -> F:
        return _document(_tag_query(_stamp(func, declaration), declaration), declaration)

    return decorate


def derived_from(callee: Callable[..., Any]) -> Callable[[F], F]:
    """Declare the decorated method as needing exactly what ``callee`` needs.

    For a wrapper whose request is a call to another declared method: the requirement is read
    from that method rather than restated, so one method owns the declaration and the other
    borrows it - there is no second copy to go stale. The docstring names the owner, because
    the columns shown below it describe the callee's request and not the wrapper's own.

    Args:
        callee: The declared method this one drives, e.g. ``Site.create_migration_ingestion_job``.

    Raises:
        ValueError: If ``callee`` names no permission - borrowing silence would produce an
            empty requirement, which is the one outcome worth failing at import time.
    """
    source = declared(callee)

    def decorate(func: F) -> F:
        stamped = _tag_query(_stamp(func, source), source)
        return _document(stamped, source, header=f"Requires what {_name(callee)} requires:")

    return decorate


def _stamp(func: F, declaration: PermissionRequirement) -> F:
    """Attach the declaration to the function, where :func:`declared` reads it back."""
    setattr(func, STAMP, declaration)
    return func


def _tag_query(func: F, declaration: PermissionRequirement) -> F:
    """Tag the query this call queues, so a denial can name what the request needed.

    The query is tagged after the call returns - or after it is awaited, since an async method
    builds its query when the coroutine runs - and only if the call actually queued a new one:
    a method that builds no request leaves the previous query, and its tag, alone.
    """

    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> Any:
        owner = args[0] if args else None
        previous = _last_query(owner)
        result: Any = func(*args, **kwargs)
        if inspect.iscoroutine(result):
            return _awaited(result, owner, previous, declaration)
        _tag(owner, previous, declaration)
        return result

    return cast(F, wrapper)


def _document(func: F, declaration: PermissionRequirement, header: str = "Requires permissions:") -> F:
    """Append what the method requires to its docstring, so ``help()`` shows it.

    Applied to the decorated callable, not to the function it wraps: a wrapper made by
    :func:`_tag_query` copies ``__doc__`` when it is created, so a later write to the inner
    function lands somewhere nobody reads.
    """
    if declaration.describe():
        func.__doc__ = f"{func.__doc__ or ''}\n\n{header}\n{textwrap.indent(declaration.describe(), '    ')}"
    return func


def _last_query(owner: Any) -> Any:
    """The query the owner's context holds now, or ``None`` if the owner has no context."""
    context = getattr(owner, "context", None)
    return getattr(context, "last_query", None) if context is not None else None


def _tag(owner: Any, previous: Any, declaration: PermissionRequirement) -> None:
    """Remember the declaration on the query this call queued, if it queued one."""
    query = _last_query(owner)
    if query is not None and query is not previous:
        query.permission_requirement = declaration


def _awaited(result: Any, owner: Any, previous: Any, declaration: PermissionRequirement) -> Any:
    """Await an async method's result, then tag the query it queued - on failure too."""

    async def run() -> Any:
        try:
            return await result
        finally:
            _tag(owner, previous, declaration)

    return run()


def _name(func: Callable[..., Any]) -> str:
    """How a call is named in an error: its qualified name, or its ``repr`` if it has none."""
    return str(getattr(func, "__qualname__", func))
