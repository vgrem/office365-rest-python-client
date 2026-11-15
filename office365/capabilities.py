"""One type's declared facts, read together instead of five times.

Planning work against a type needs five answers about it: what its columns are and which
of them the service owns (shape), what each entry point needs from the tenant
(permissions, and on the same declaration its licences), which ceilings apply (limits),
which query options its endpoint refuses (queries), and which of its methods are
commands rather than helpers (verbs). All five are declared already -
``@odata``/``@facet`` on the model, ``@require_permission`` beside the request it
describes, ``@limit`` on the class or the method, ``@query_capabilities`` on the
collection, ``@verb`` on the method - but they are declared in five places, so a report,
a preflight and a plan that wants all five either imports five modules and reassembles
them or keeps a sixth copy of the answer.

:func:`capabilities_of` is that reassembly, once and read-only: it declares nothing and
sends nothing, it asks the modules that own the facts. Ask it about a type and it answers
the schema, the entry points that name a permission, the limits, the query rules and the
commands; ask it about one call and it answers for that call, with no schema (a method
has no columns) and no query rules (those belong to the collection that issues the query).

Two silences are deliberate. It does not decide what a missing fact means - a type whose
entry points name no permission is reported that way, not repaired and not refused,
because only the caller knows whether the omission matters. And it does not turn a
licence into a SKU: :attr:`Capabilities.licenses` is the union of the service plans the
declarations name, which is the vocabulary
:mod:`office365.permissions.catalog` already checks against.

    >>> from office365.capabilities import capabilities_of
    >>> from office365.communications.callrecords.collection import CallRecordCollection
    >>> caps = capabilities_of(CallRecordCollection)
    >>> caps.queries.supports("top")
    False

:func:`hints_of` is the same join said out loud: one command's permission, the confirmation
its effect implies, its licences, whether only the beta root answers it, and whether the
type declares a form that walks every page -- a sentence each, for a help page to print.
"""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Any, Mapping, Optional, Tuple

from office365.permissions.declaration import STAMP, PermissionRequirement
from office365.runtime.limits import LimitDecl, limits_of
from office365.runtime.query_capabilities import QueryCapability, query_capabilities_of
from office365.runtime.schema import TypeSchema
from office365.runtime.verbs import VerbMeta, paged_of, verbs_of


@dataclass(frozen=True)
class Capabilities:
    """The declared facts about one type, or about one of its calls."""

    #: Where it lives, spelled as :attr:`office365.permissions.index.Operation.fqn` spells
    #: it: ``office365.onedrive.driveitems.driveItem:DriveItem``.
    name: str
    #: The class or callable that was asked about, so a report can re-ask it.
    target: Any
    #: The shape, or ``None`` for a callable. A collection answers with no columns: the
    #: columns belong to the type it collects.
    schema: Optional[TypeSchema]
    #: Attribute name -> what it needs. Inherited declarations are included, and a
    #: subclass that re-declares a name replaces the one it inherits.
    declarations: Mapping[str, PermissionRequirement]
    #: Ceilings on the class itself, on its properties and methods, and (for a callable)
    #: on the arguments it enforces them against. Kept as declarations so ``arg`` survives.
    limits: Tuple[LimitDecl, ...]
    #: The query rules of the collection that issues the query, or ``None`` when the
    #: target declares none - which is every type that is not a collection.
    queries: Optional[QueryCapability]
    #: Attribute name -> the command the method is. Empty is the ordinary answer: the
    #: stamp is opt-in, so a method that declares nothing is a shaping helper or a path
    #: builder rather than a command. A ``role`` on one member and not on another is how
    #: a type says which of its entry points a caller may drive.
    verbs: Mapping[str, VerbMeta]
    #: Attribute name of the command that walks every page, or ``None`` for one page.
    #: ``get_all`` declares ``paged=True, expose=False``: the same noun as ``list``,
    #: longer -- so this is the name a ``--all`` flag reaches, never a command word.
    paged: Optional[str]

    @property
    def licenses(self) -> Tuple[str, ...]:
        """Every service plan the declarations name, once each."""
        named = {plan for declaration in self.declarations.values() for plan in declaration.licenses}
        return tuple(sorted(named))


def capabilities_of(target: Any) -> Capabilities:
    """Every declared fact about ``target``, a type or one of its calls.

    Args:
        target: A class, answered for its shape, its declarations, its limits and its
            query rules; or a callable (a method, or a decorated property's getter),
            answered for that call alone.

    Raises:
        TypeError: ``target`` is neither, so there is no fact to report and an empty
            answer would read as "this type declares nothing".
    """
    if isinstance(target, type):
        return Capabilities(
            name=_fqn(target),
            target=target,
            schema=TypeSchema.of(target),
            declarations=_declarations_of(target),
            limits=limits_of(target),
            queries=query_capabilities_of(target),
            verbs=verbs_of(target),
            paged=_paged_name(target),
        )
    if callable(target):
        declaration = _declaration_of(target)
        return Capabilities(
            name=_fqn(target),
            target=target,
            schema=None,
            declarations=MappingProxyType({_member_name(target): declaration} if declaration else {}),
            limits=limits_of(target),
            queries=None,
            verbs=verbs_of(target),
            paged=_paged_name(target),
        )
    raise TypeError(f"capabilities_of asks about a type or a callable, not {type(target).__name__}")


def hints_of(target: Any, method: str) -> Tuple[str, ...]:
    """What a caller should know before running one command, a sentence each.

    Five facts, all declared already and none of them new: the permission stamped on the
    method (or the honest absence of one), whether the verb's effect makes it the kind of
    command that is confirmed first, whether the type is preview-only (``@version("beta")``,
    so only the beta root answers it), whether the type declares a form that walks every
    page, and the licences the declaration names.

    This is the join a help page prints, and the reason it is a function rather than five
    questions asked in the consumer: asked separately, four of the five are one call each
    and the fifth is the one that gets forgotten (``confirm`` is a property nobody read).

    Read it, do not parse it. A caller that needs the answer as data has ``capabilities_of``
    and does not need this: ``confirm`` is a flag there, and a licence is a tuple.
    """
    capabilities = capabilities_of(target)
    declaration = capabilities.declarations.get(method)
    verb = capabilities.verbs.get(method)
    if verb is None:
        raise ValueError(
            f"{method} names no verb: hints_of answers for a command, and a method that declares "
            "none is not one -- decorate it with @verb(role=...) or leave it out of the help page"
        )
    lines = [
        declaration.to_hint() if declaration is not None else "Declares no permission.",
    ]
    if verb.confirm:
        lines.append(f"Confirmed before it is sent: it {verb.effect}s what the service holds.")
    if declaration is not None and declaration.licenses:
        lines.append(f"Needs one of these licences: {', '.join(declaration.licenses)}.")
    if capabilities.schema is not None and capabilities.schema.versions == frozenset({"beta"}):
        lines.append("Only the beta root answers it.")
    if capabilities.paged is not None:
        lines.append(f"{capabilities.paged} walks every page.")
    return tuple(line for line in lines if line)


def _paged_name(target: Any) -> Optional[str]:
    """The one command that walks every page, if the target declares one."""
    return next(iter(paged_of(target)), None)


def _declarations_of(cls: type) -> Mapping[str, PermissionRequirement]:
    """The declarations on ``cls`` and its bases, the nearest one per name.

    Walked from the base down so an override that declares nothing does not hide the
    declaration it overrides: a subclass that restates the request without restating
    the permission still answers what the request needs.
    """
    found: dict[str, PermissionRequirement] = {}
    for klass in reversed(cls.__mro__):
        for name, member in vars(klass).items():
            declaration = _declaration_of(member)
            if declaration is not None:
                found[name] = declaration
    return MappingProxyType(found)


def _declaration_of(member: Any) -> Optional[PermissionRequirement]:
    """The declaration stamped on a member, reading through a property's getter."""
    if isinstance(member, property):
        member = member.fget
    declaration = getattr(member, STAMP, None)
    return declaration if isinstance(declaration, PermissionRequirement) else None


def _member_name(member: Any) -> str:
    """The name a member answers to, without the class it belongs to."""
    qualified = getattr(member, "__qualname__", None) or getattr(member, "__name__", str(member))
    return qualified.rsplit(".", 1)[-1]


def _fqn(target: Any) -> str:
    """``module:Qualname``, the spelling the permission index uses."""
    qualified = getattr(target, "__qualname__", None) or getattr(target, "__name__", str(target))
    return f"{getattr(target, '__module__', '')}:{qualified}"


__all__ = ["Capabilities", "capabilities_of", "hints_of"]
