"""Finding a type by the words a command line uses.

``outlook message list`` names three things, and two of them are declarations: the verb is
stamped on the method (:mod:`office365.runtime.verbs`) and the product is stated by the
package (:func:`office365.runtime.schema.service_of`). The noun is the type's own name,
singular, because that is what a type is called - ``outlook message list`` reads like
``az vm list`` - so nothing here spells a word the model already holds, and nothing here is
a list of commands. What this module does is pair the two halves of one noun and read:

* the type a feed holds, from ``ClientObjectCollection.item_type()``, which the base
  declares (``MessageCollection(DeltaCollection["Message"])``);
* the commands a type answers, from ``verbs_of`` over its stamped methods;
* the product a type belongs to, from ``service_of`` over its module.

Two words are one word when they carry the same letters, so ``message-rule``,
``message_rule`` and ``MessageRule`` all fold to ``messagerule``. The tree does not settle
its own separators (``cloud_pc.py`` sits beside ``share_point_audit_record.py``), and a
command line is the wrong place to decide what the library has not.

Discovery stays inside the product a command names: the whole tree costs ~3 s to import,
one product 0.2 s (``outlook``) to 1.2 s (``sharepoint``), and the index is kept once built.
"""

from __future__ import annotations

import importlib
import pkgutil
import re
from collections.abc import Iterator, Mapping
from dataclasses import dataclass, replace
from difflib import get_close_matches
from functools import cache
from types import MappingProxyType, ModuleType

from office365.runtime.client_object import ClientObject
from office365.runtime.client_object_collection import ClientObjectCollection
from office365.runtime.verbs import VerbMeta, command_word, verbs_of

#: ``list`` reads the feed and ``create`` posts into it, so both are looked for on the
#: collection first; every other command - ``action`` included - acts on one item.
COLLECTION_ROLES = frozenset({"list", "create"})


@dataclass(frozen=True)
class Route:
    """What a command line resolved to: one noun, and the half a verb was found on.

    :attr:`entity` is the item and :attr:`collection` the feed that holds it, ``None`` for a
    type that states no feed (a report root, a workbook function). :attr:`verb` and
    :attr:`target` are filled in only when an action was asked for, and they are the
    declaration and the class that answers it, so a caller sends through a type instead of
    looking a name up a second time.
    """

    product: str
    noun: str
    entity: type
    collection: type | None = None
    verb: VerbMeta | None = None
    target: type | None = None


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
    order = (found.collection, found.entity) if action in COLLECTION_ROLES else (found.entity, found.collection)
    answers: dict[str, tuple[type, VerbMeta]] = {}
    for half in reversed([half for half in order if half is not None]):
        answers.update({meta.name: (half, meta) for meta in verbs_of(half).values() if meta.expose})
    if action not in answers:
        raise LookupError(f"{product} {noun} does not answer {action!r}; it answers: {', '.join(sorted(answers))}")
    return replace(found, verb=answers[action][1], target=answers[action][0])


@cache
def nouns(product: str) -> Mapping[str, Route]:
    """Every noun ``product`` publishes, keyed by the letters a command line spells.

    Read from the product's own package and nothing else. A feed names the type it holds in
    its generic base, or, when that is stated lazily to break a circular import, in its own
    name - which the tree keeps true for all ten feeds whose base is silent - and the item
    is filed under the feed so both halves answer one noun.
    """
    package = _package(product)
    declared = list(_declared_in(package))
    known: dict[str, type] = {}
    for cls in declared:
        known.setdefault(cls.__name__, cls)
    held: dict[type, type | None] = {}
    for cls in declared:
        if issubclass(cls, ClientObjectCollection):
            item = cls.item_type() or known.get(cls.__name__.removesuffix("Collection"))
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
