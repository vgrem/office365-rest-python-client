"""What a method *is*, when it is a command.

The type system answers what an object has: its columns, which of them a request may
carry, which one names it, which links lead out of it. It does not answer what a *method*
is, and a caller driving the library from outside Python needs that answer before it can
build a command line: may this be sent to a tenant, is it a read or a write, does it need
confirming, does it follow paging until the feed ends.

That fact belongs on the method, for the reason ``@require_permission`` and ``@limit``
live there: it is a property of the call, not of the column the call touches. So
``@verb`` stamps it, :func:`declared_verb` reads it back, and :func:`verbs_of` walks a
class the way ``_declarations_of`` walks permissions - three functions, one meaning.

Two silences are deliberate. The stamp is **opt-in**: a method that declares nothing is
not a command, which is the honest answer for the ~4,000 public methods that build paths,
shaping helpers or intermediate objects. And the effect is **inferred from the role**,
because ``list`` cannot be anything but a read and ``delete`` cannot be anything but a
destroy; only ``action`` has to say, since an OData action's effect is a fact about the
service, not about the spelling of its name.
"""

from __future__ import annotations

import re
from collections.abc import Callable, Mapping
from dataclasses import dataclass, replace
from types import MappingProxyType
from typing import Any, TypeVar, cast

F = TypeVar("F", bound=Callable[..., Any])

#: Where the declaration is visible on a decorated method. Read it with
#: :func:`declared_verb`, which explains what a missing one means.
STAMP = "__verb__"

#: What a command can do to the object it names. ``list`` and ``get`` read, ``create``
#: and ``update`` write, ``delete`` destroys, and ``action`` is whatever the service says
#: - which is why only it has to state an effect.
ROLES = ("list", "get", "create", "update", "delete", "action")

#: The effect, in the vocabulary a safety gate uses: may send (``read``), changes
#: something (``write``), is irreversible (``destroy``, and therefore confirmed), or acts
#: on the session alone (``local``, which is the one effect a caller may reach with no
#: session at all - logging in is the only member of that set today).
EFFECTS = ("read", "write", "destroy", "local")

_EFFECT_BY_ROLE = {
    "list": "read",
    "get": "read",
    "create": "write",
    "update": "write",
    "delete": "destroy",
}


@dataclass(frozen=True)
class VerbMeta:
    """One method's command facts.

    :attr:`name` is the command word; empty means "the method's own name, kebab-cased",
    which is what almost every method wants. It is stated on the few whose Python name
    is not a command word - ``delete_object`` answers ``delete``.

    :attr:`mode` distinguishes sibling declarations that share one command word, which is
    how six ways to log in stay one ``login``: filled from the method name (``with_``
    dropped) unless stated, since a method is named after the way it authenticates.

    :attr:`paged` and :attr:`lro` are tri-state on purpose: ``None`` means "infer it
    from what the method returns", ``True``/``False`` overrides the inference. That is
    the same rule as everywhere else here - declare only where the code does not already
    say it.
    """

    role: str
    name: str = ""
    effect: str = ""
    mode: str = ""
    expose: bool = True
    paged: bool | None = None
    lro: bool | None = None

    def __post_init__(self) -> None:
        if self.role not in ROLES:
            raise ValueError(f"unknown verb role {self.role!r}; known: {', '.join(ROLES)}")
        effect = self.effect or _EFFECT_BY_ROLE.get(self.role, "")
        if effect not in EFFECTS:
            raise ValueError(
                f"role {self.role!r} states no effect; pass effect={'|'.join(EFFECTS)} "
                "because the service, not the name, decides what it does"
            )
        object.__setattr__(self, "effect", effect)

    @property
    def needs_session(self) -> bool:
        """Whether the command needs a session before it can run.

        Derived from the effect, so there is one place to state it: everything but
        ``local`` touches the tenant and therefore a token, and ``local`` acts on the
        session itself - which is why a caller can be told to ``login`` first.
        """
        return self.effect != "local"

    @property
    def confirm(self) -> bool:
        """Whether the command must be confirmed before it is sent.

        Inferred, never declared: an irreversible command is the one that asks. A
        declared ``confirm`` would be a second place to keep the same answer, and the
        cheap mistake - adding ``destroy`` and forgetting the flag - is the one worth
        making impossible.
        """
        return self.effect == "destroy"


def verb(**meta: Any) -> Callable[[F], F]:
    """Declare that a method is a command, and which one.

    Usage::

        @verb(role="delete")  # a DELETE, confirmed by the caller
        def delete_object(self, **kwargs): ...


        @verb(role="list", paged=True)  # follows @odata.nextLink until the end
        def get_all(self, page_size=None): ...


        @verb(role="action", effect="write")  # an OData action; the effect is stated
        def send(self): ...

    Args:
        meta: The fields of :class:`VerbMeta`: ``role`` (required), and optionally
            ``name``, ``effect``, ``expose``, ``paged`` and ``lro``.
    """
    declaration = VerbMeta(**meta)

    def decorator(func: F) -> F:
        setattr(func, STAMP, declaration)
        return func

    return decorator


def declared_verb(func: Any) -> VerbMeta:
    """The command ``func`` declares, named, or a loud failure naming it.

    This is the only way to read a declaration. A method that declares nothing is not a
    command, so asking anyway is a mistake and gets an exception instead of a command
    with no name, no effect and nothing to confirm.
    """
    declaration = _stamp_on(func)
    if declaration is None:
        raise ValueError(
            f"{_name(func)} names no verb: decorate it with @verb(role=...) to make it a command, "
            "or leave it undeclared if it is not one"
        )
    word = command_word(func)
    # Only a ``with_`` method is named after the way it authenticates, so only it
    # carries a mode; the rest of the tree leaves the field alone.
    mode = declaration.mode or (word[5:] if word.startswith("with-") else "")
    return replace(declaration, name=declaration.name or word, mode=mode)


def verbs_of(target: Any) -> Mapping[str, VerbMeta]:
    """The commands a class declares, keyed like its attributes.

    Walked from the base down, so an override that declares nothing does not hide the
    command it overrides: a collection that restates ``get_all`` without restating the
    verb still answers it. The nearest declaration wins, as it does for permissions.
    """
    if not isinstance(target, type):
        declaration = _stamp_on(target)
        return MappingProxyType({}) if declaration is None else MappingProxyType({_name(target): declared_verb(target)})
    found: dict[str, VerbMeta] = {}
    for klass in reversed(target.__mro__):
        for name, member in vars(klass).items():
            if _stamp_on(member) is not None:
                found[name] = declared_verb(member)
    return MappingProxyType(found)


def _stamp_on(member: Any) -> VerbMeta | None:
    """The declaration stamped on a member, reading through a property's getter."""
    if isinstance(member, property):
        member = member.fget
    declaration = getattr(member, STAMP, None)
    return cast("VerbMeta | None", declaration if isinstance(declaration, VerbMeta) else None)


def _name(member: Any) -> str:
    """The name a member answers to, without the class it belongs to."""
    qualified = getattr(member, "__qualname__", None) or getattr(member, "__name__", str(member))
    return qualified.rsplit(".", 1)[-1]


def command_word(target: Any) -> str:
    """``delete_object`` -> ``delete-object``: the spelling a command line uses.

    A run of capitals is one word, so the break falls before its last capital
    (``CloudPC`` -> ``cloud-pc``, ``AADUser`` -> ``aad-user``) rather than between every
    pair of them. The tree writes the same names in a file, so this is the one spelling a
    command line and a help page share.
    """
    word = re.sub(r"(?<=[a-z0-9])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])", "-", _name(target).strip("_"))
    return word.replace("_", "-").lower()


__all__ = ["EFFECTS", "ROLES", "STAMP", "VerbMeta", "command_word", "declared_verb", "verb", "verbs_of"]
