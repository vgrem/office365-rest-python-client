"""Finding a type by the words a command line uses.

``outlook messages list`` names three things: a product, a noun and a verb. The verb is
already a declaration on the method (:mod:`office365.runtime.verbs`), and the product is
already a declaration on the package (:func:`office365.runtime.schema.service_of`), so
neither needs a table. The noun is the one word with no declaration anywhere - a command
line says ``message``, the type is called ``Message`` - so this module derives it from the
type it belongs to, and resolves the collection that holds it as the same noun. It is the
singular, because that is what the type is called: ``outlook message list`` reads like
``az vm list``, and nothing here has to know English plurals.

Two words are the same word when they carry the same letters. ``message-rule``,
``message_rule`` and ``MessageRule`` all fold to ``messagerule``, so a command line may
spell a noun the way it reads best and never be told it guessed the separators wrong -
the separators are the one thing the type system does not decide for it.

The pairing is the part worth stating. A collection says which type it holds - in its
generic base (``ClientObjectCollection[Message]``) sometimes lazily, or by carrying the
type in its name (``MessageCollection``) - so the two halves of one noun are read, never
assumed. Where two classes answer one noun - 16 of 1,978 do, ``User`` beside ``User``
under ``sharepoint.directory`` and ``sharepoint.principal``, ``B2xIdentityUserFlow`` beside
``B2XIdentityUserFlow`` - the answer is a ranking
(a class a command can list, then the shorter path, then the alphabet), not a table:
the same words answer the same type on every run, and nothing has to be kept in step
with a class that is added tomorrow.

Discovery is per product, because it has to be cheap: importing the whole tree costs ~3 s,
while one product costs a fraction of it (cold, interpreter included: ``outlook`` 0.21 s,
``teams`` 0.44 s, ``sharepoint`` 1.20 s). So :func:`nouns` walks one package and remembers
the answer, and a command never pays for a product it does not mention.
"""

from __future__ import annotations

import importlib
import pkgutil
import re
import sys
import typing
from collections.abc import Iterator, Mapping
from dataclasses import dataclass
from difflib import get_close_matches
from functools import cache
from types import MappingProxyType

from office365.runtime.client_object import ClientObject
from office365.runtime.client_object_collection import ClientObjectCollection
from office365.runtime.verbs import VerbMeta, command_word, verbs_of

#: The roles that address the collection rather than the item: ``list`` reads the feed,
#: ``create`` posts into it. Everything else - including ``action``, which is why it is
#: looked up on both halves - acts on one item.
_COLLECTION_ROLES = frozenset({"list", "create"})


@dataclass(frozen=True)
class Route:
    """One noun, resolved to the types a command word can be sent to.

    :attr:`entity` is the item and :attr:`collection` the feed that holds it, which may be
    ``None`` when the type states no collection (a report, a workbook function). When a
    verb was asked for, :attr:`verb` is its declaration and :attr:`target` the half that
    declares it - the object a caller sends through, not a name to look up again.
    """

    product: str
    noun: str
    entity: type
    collection: type | None
    verb: VerbMeta | None = None
    target: type | None = None


def route(product: str, noun: str, action: str = "") -> Route:
    """The types ``<product> <noun> <action>`` names, or a failure saying what was close.

    Raises:
        LookupError: the product imports nothing, the noun is not spelled that way, or no
            exposed verb on either half answers ``action``. The message lists what does
            exist, because a command line's job is to be tried.
    """
    index = nouns(product)
    key = _fold(noun)
    found = index.get(key)
    if found is None:
        spoken = {_fold(entry.noun): entry.noun for entry in index.values()}
        near = get_close_matches(key, spoken, n=5)
        spoken_near = ", ".join(spoken[one] for one in near)
        raise LookupError(f"no {noun!r} in {product!r}" + (f"; did you mean {spoken_near}?" if near else ""))
    if not action:
        return found
    order = (found.collection, found.entity) if action in _COLLECTION_ROLES else (found.entity, found.collection)
    halves = [half for half in order if half is not None]
    for half in halves:
        for meta in verbs_of(half).values():
            if meta.expose and meta.name == action:
                return Route(found.product, found.noun, found.entity, found.collection, meta, half)
    available = sorted({meta.name for half in halves for meta in verbs_of(half).values() if meta.expose})
    raise LookupError(f"{product} {noun} does not answer {action!r}; it answers: {', '.join(available)}")


@cache
def nouns(product: str) -> Mapping[str, Route]:
    """Every noun ``product`` publishes, keyed by the word a command line spells.

    Built by importing that product's package and nothing else, then reading each class's
    own declarations: its name for the noun, its generic base for the type its collection
    holds. The answer is cached per product, so a shell pays once.
    """
    try:
        package = importlib.import_module(f"office365.{product}")
    except ModuleNotFoundError as err:
        raise LookupError(f"no product {product!r}") from err
    if not hasattr(package, "__path__"):
        raise LookupError(f"no product {product!r}: {product} is a module, not a product")
    entities: dict[str, list[type]] = {}
    collections: dict[str, list[type]] = {}
    for cls in _declared_in(package):
        bucket = collections if issubclass(cls, ClientObjectCollection) else entities
        bucket.setdefault(cls.__name__, []).append(cls)
    candidates: dict[str, list[tuple[type, type | None]]] = {}
    for name, group in collections.items():
        stem = name[: -len("Collection")] if name.endswith("Collection") else name
        for collection in group:
            held = _item_type(collection)
            for entity in [held] if held is not None else entities.get(stem, []):
                candidates.setdefault(_fold(_noun_of(entity, product)), []).append((entity, collection))
    for group in entities.values():
        for entity in group:
            candidates.setdefault(_fold(_noun_of(entity, product)), []).append((entity, None))
    found: dict[str, Route] = {}
    for key, options in candidates.items():
        entity, collection = _ranked(options)
        found[key] = Route(product, _noun_of(entity, product), entity, collection)
    return MappingProxyType(found)


def _ranked(options: list[tuple[type, type | None]]) -> tuple[type, type | None]:
    """The one owner of a noun the tree reuses under one name.

    Sixteen nouns are spelled by two classes - ``User`` exists under ``sharepoint.directory``
    and under ``sharepoint.principal``, ``Group`` beside ``Group`` - and a name is not an
    identity, so one of them has to be the answer. It is a *ranking*, not a table: the class
    a command can list (the one with a collection) wins, then the shorter module path, then
    the alphabet. A rule, so the same words always answer the same type on every run.
    """
    return min(options, key=lambda option: (option[1] is None, option[0].__module__.count("."), option[0].__module__))


def _declared_in(package: typing.Any) -> Iterator[type]:
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


def _item_type(collection: type) -> type | None:
    """The type a collection states it holds, from its generic base.

    The base may state it lazily (``DeltaCollection[ForwardRef('Message')]``), so a name is
    resolved in the collection's own module - the scope the class was written in.
    """
    for base in getattr(collection, "__orig_bases__", ()):
        origin = typing.get_origin(base)
        if not (isinstance(origin, type) and issubclass(origin, ClientObjectCollection)):
            continue
        arguments = typing.get_args(base)
        if not arguments:
            continue
        argument = arguments[0]
        if isinstance(argument, type):
            return argument
        scope = sys.modules.get(collection.__module__)
        resolved = getattr(scope, getattr(argument, "__forward_arg__", ""), None) if scope else None
        if isinstance(resolved, type):
            return resolved
    return None


def _noun_of(entity: type, product: str) -> str:
    """The noun ``entity`` answers, with the product word it repeats left off.

    ``planner.tasks.task:PlannerTask`` is ``planner task``, not ``planner planner-task``:
    the leading ``Planner`` is the product already spelled earlier on the line, which is the
    same rule the generator follows when it drops a word the module path implies. Only the
    *product* is stripped - ``DriveItem`` keeps its ``drive`` under ``onedrive``, because
    nothing in the type system says the word is redundant there.
    """
    word = command_word(entity.__name__)
    head = command_word(product) + "-"
    return word[len(head) :] if word.startswith(head) and len(word) > len(head) else word


def _fold(word: str) -> str:
    """``MessageRule``, ``message-rule``, ``message_rule`` -> ``messagerule``: one key.

    The separators a command line puts between words are a reading preference, and the tree
    does not settle them (``cloud_pc.py`` beside ``share_point_audit_record.py``), so they
    are dropped on both sides rather than decided here. Case goes too, because a shell is
    not case sensitive about a noun.
    """
    return re.sub(r"[^a-z0-9]", "", word.lower())
