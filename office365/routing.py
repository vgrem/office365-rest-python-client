"""Finding a type by the words a command line uses.

A command line is ``<product> <noun> <verb> <arguments>``, and the first three levels are
already statements of the model, so none of them is spelled a second time here:

* the product is the package a type lives in, and the package says so (``__product__``, read
  by :func:`office365.runtime.schema.service_of`);
* the noun is the type's own name, singular - ``outlook message list`` reads like
  ``az vm list`` - and a feed answers the same noun because it states what it holds
  (``ClientObjectCollection.item_type()``);
* the verb is stamped on the method (:mod:`office365.runtime.verbs`), and the arguments are
  that method's own parameters.

Two words are one word when they carry the same letters, so ``message-rule``,
``message_rule`` and ``MessageRule`` all fold to ``messagerule``. The tree does not settle
its own separators (``cloud_pc.py`` sits beside ``share_point_audit_record.py``), and a
command line is the wrong place to decide what the library has not.

A route is walked, not built: :func:`chain` reads the return annotations from the root
down, so a command reaches the object the model already connects instead of composing a URL.

Discovery stays inside the product a command names: the whole tree costs ~3 s to import,
one product 0.2 s (``outlook``) to 1.2 s (``sharepoint``), and the index is kept once built.
"""

from __future__ import annotations

import importlib
import pkgutil
import re
import typing
from collections.abc import Iterator, Mapping
from dataclasses import dataclass, replace
from difflib import get_close_matches
from functools import cache, cached_property
from types import MappingProxyType, ModuleType

from office365.runtime.client_object import ClientObject
from office365.runtime.client_object_collection import ClientObjectCollection
from office365.runtime.verbs import VerbMeta, command_word, verbs_of


@dataclass(frozen=True)
class Route:
    """What a command line resolved to: one noun, and the half a verb was found on.

    :attr:`entity` is the item and :attr:`collection` the feed that holds it, ``None`` for a
    type that states no feed. The last three are filled in only when an action was asked for:
    the declaration, the class that answers it and the attribute on it, so a caller reads the
    arguments of the method that will do the work instead of looking it up a second time.
    """

    product: str
    noun: str
    entity: type
    collection: type | None = None
    verb: VerbMeta | None = None
    target: type | None = None
    method: str = ""

    @cached_property
    def commands(self) -> "Mapping[str, tuple[type, str, VerbMeta]]":
        """Action -> the half that answers it, the attribute on it, and the declaration.

        The item is asked first, then its feed; they never disagree (a feed restates the verb it
        inherits), and the declaration says which half means what.
        """
        answers: dict[str, tuple[type, str, VerbMeta]] = {}
        for half in (self.entity, self.collection):
            if half is not None:
                for method, meta in verbs_of(half).items():
                    if meta.expose:
                        answers.setdefault(meta.name, (half, method, meta))
        return MappingProxyType(answers)


def route(product: str, noun: str, action: str = "") -> Route:
    """The type ``<product> <noun> <action>`` names, or a failure saying what was close.

    Raises:
        LookupError: the product publishes no types, the noun is spelled with other letters,
            or no exposed command on either half answers ``action``. The message lists what
            does exist, because a command line's job is to be tried.
    """
    index = nouns(product)
    key = _fold(noun)
    found = index.get(key)
    if found is None:
        spoken = {_fold(entry.noun): entry.noun for entry in index.values()}
        near = ", ".join(spoken[one] for one in get_close_matches(key, spoken, n=5))
        raise LookupError(f"no {noun!r} in {product!r}" + (f"; did you mean {near}?" if near else ""))
    if not action:
        return found
    if action not in found.commands:
        spoken = ", ".join(sorted(found.commands))
        raise LookupError(f"{product} {noun} does not answer {action!r}; it answers: {spoken}")
    target, method, verb = found.commands[action]
    return replace(found, verb=verb, target=target, method=method)


def chain(root: object, target: type) -> tuple[str, ...] | None:
    """The attributes to walk from ``root`` to an instance of ``target``, or ``None``.

    A command line names a type; a request needs an object hanging off the client, and the
    route between them is already written down: every link is a property that says what it
    returns. So the walk reads return annotations and nothing else - ``GraphClient.me``
    answers ``User``, ``User.messages`` answers ``MessageCollection`` - and a generic feed
    is read through its origin, because ``EntityCollection[Note]`` holds an
    ``EntityCollection`` at run time whatever the parameter says.

    Breadth first, so the path is the shortest one and the first noun the model can reach is
    the one a user gets. ``root`` may be the client class, because the walk reads types only
    and a command has to name its own route before it holds a token. ``None`` is the honest
    answer for the rest: 588 types are constructed nowhere, and no command line should invent
    a URL to reach them.
    """
    start = root if isinstance(root, type) else type(root)
    seen = {start}
    queue: list[tuple[type, tuple[str, ...]]] = [(start, ())]
    while queue:
        cls, path = queue.pop(0)
        for attribute, held in _links(cls).items():
            if held is target:
                return path + (attribute,)
            if held not in seen:
                seen.add(held)
                queue.append((held, path + (attribute,)))
    return None


@cache
def _links(cls: type) -> Mapping[str, type]:
    """Attribute -> the client object it holds, for the links a walk may take.

    A getter that needs an argument is not a link: the walk has nothing to pass it, and the
    60 links that take one ``id`` are addressed by a flag, not by walking.
    """
    links: dict[str, type] = {}
    for klass in reversed(cls.__mro__):
        for name, member in vars(klass).items():
            if not isinstance(member, property) or member.fget is None:
                continue
            code = member.fget.__code__
            if code.co_argcount != 1 or code.co_kwonlyargcount:
                continue
            try:
                hint = typing.get_type_hints(member.fget).get("return")
            except NameError:  # a name the getter's module cannot import is not a route
                continue
            held = typing.get_origin(hint) or hint
            if isinstance(held, type) and issubclass(held, ClientObject):
                links.setdefault(name, held)
    return MappingProxyType(links)


@cache
def nouns(product: str) -> Mapping[str, Route]:
    """Every noun ``product`` publishes, keyed by the letters a command line spells.

    Read from the product's own package and nothing else. A feed names the type it holds in
    its generic base, and a name stated there to break a circular import is resolved against
    the product's own types, so the item is filed under the feed and both halves answer one
    noun. Nothing is spelled out twice: a noun is the name of a type.
    """
    package = _package(product)
    declared = list(_declared_in(package))
    known: dict[str, type] = {}
    for cls in declared:
        known.setdefault(cls.__name__, cls)
    held: dict[type, type | None] = {}
    for cls in declared:
        if issubclass(cls, ClientObjectCollection):
            item = cls.item_type(known)
            if item is not None:
                held[item] = cls
        else:
            held.setdefault(cls, None)
    grouped: dict[str, list[Route]] = {}
    for entity, collection in held.items():
        noun = _noun_of(entity, product)
        grouped.setdefault(_fold(noun), []).append(Route(product, noun, entity, collection))
    return MappingProxyType({key: _ranked(options) for key, options in grouped.items()})


def _package(product: str) -> ModuleType:
    """The package a product word names, or a failure naming what is not one."""
    try:
        package = importlib.import_module(f"office365.{product}")
    except ModuleNotFoundError as err:
        raise LookupError(f"no product {product!r}") from err
    if not hasattr(package, "__path__"):
        raise LookupError(f"{product!r} is a module, not a product")
    return package


def _declared_in(package: ModuleType) -> Iterator[type]:
    """The client objects whose own module is inside ``package``.

    Read from each module's namespace rather than by walking the type tree, and filtered on
    ``__module__`` so a type another module owns is not claimed twice.
    """
    prefix = package.__name__ + "."
    for info in pkgutil.walk_packages(package.__path__, prefix):
        try:
            module = importlib.import_module(info.name)
        except Exception:  # a model module that cannot import publishes nothing
            continue
        for member in vars(module).values():
            if isinstance(member, type) and member.__module__ == info.name and issubclass(member, ClientObject):
                yield member


def _ranked(options: list[Route]) -> Route:
    """The one owner of a noun the tree reuses under one name.

    Sixteen nouns are spelled by two classes - ``User`` under ``sharepoint.directory`` and
    under ``sharepoint.principal``, ``Group`` beside ``Group`` - and a name is not an
    identity, so one of them has to be the answer. It is a *ranking*, not a table: the class
    a command can list wins, then the shorter module path, then the alphabet, so the same
    words answer the same type on every run.
    """
    return min(
        options,
        key=lambda found: (found.collection is None, found.entity.__module__.count("."), found.entity.__module__),
    )


def _noun_of(entity: type, product: str) -> str:
    """The noun ``entity`` answers, with the product word it repeats left off.

    ``planner.tasks.task:PlannerTask`` is ``planner task``, not ``planner planner-task``:
    the leading ``Planner`` is the product already spelled earlier on the line, the same rule
    the generator follows when it drops a word the module path implies. Only the product word
    is stripped - ``DriveItem`` keeps its ``drive`` under ``onedrive``, because nothing in
    the type system says the word is redundant there.
    """
    word = command_word(entity.__name__)
    head = command_word(product) + "-"
    return word[len(head) :] if word.startswith(head) and len(word) > len(head) else word


def _fold(word: str) -> str:
    """``MessageRule``, ``message-rule``, ``message_rule`` -> ``messagerule``: one key.

    The separators a command line puts between words are a reading preference, and case is
    not something a shell is careful about, so both are dropped on both sides rather than
    decided here.
    """
    return re.sub(r"[^a-z0-9]", "", word.lower())
