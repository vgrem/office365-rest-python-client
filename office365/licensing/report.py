"""Which licences this tree's commands need, and whether a tenant holds them.

The markers say what a *type* requires (:mod:`office365.permissions.declaration`), and the index
says which nouns a command line can reach - each record carrying the marker's own answer as
``licence``. This module is the join between those two facts and the tenant's
``subscribedSkus``: a plan is either held or it is not, and a reader can see which words that
buys before typing them.

Nothing here imports the model or sends a request. The input is a parsed index document and the
plan names a caller has already read, so the report costs no round trip of its own and is
testable without a tenant. What it must never become is a second catalogue: which products sell
which plan is Microsoft's published data, and the only live fact used here is the tenant's own
``subscribedSkus``.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from typing import Any

from office365.permissions.declaration import USER

#: How many package segments name a family. ``office365.intune.devices.management.managed`` is
#: ``intune.devices``: deep enough to tell devices from policies, shallow enough that a module
#: path does not become a report line.
FAMILY_DEPTH = 2

#: The answers a row can carry. ``unknown`` is not a maybe: it is what a read that failed says,
#: and it is never turned into a refusal (an unread answer is not a "no").
YES, NO, UNKNOWN = "yes", "no", "unknown"

#: The cells a table shows, in order: what it is called, whose seat holds it, whether this tenant
#: has it, and how much of the tree it opens.
COLUMNS = ("plan", "seat", "held", "nouns", "families")


@dataclass(frozen=True)
class Family:
    """The nouns of one area, and the licence every one of them declares.

    :attr:`nouns` counts the command words, not the classes: two classes that spell one noun are
    one word to type, and the report is about what a person can run.
    """

    name: str
    nouns: int
    plans: tuple[str, ...]
    seat: str


@dataclass(frozen=True)
class Licence:
    """One licence the tree names, the seat that must hold it, and the areas that need it."""

    plans: tuple[str, ...]
    seat: str
    families: tuple[Family, ...]

    @property
    def name(self) -> str:
        """The plan name, or the alternatives when the marker accepted any one of several."""
        return " | ".join(self.plans)

    @property
    def nouns(self) -> int:
        return sum(family.nouns for family in self.families)


def of(document: Mapping[str, Any]) -> tuple[Licence, ...]:
    """The licences the index names, the one that opens the most words first.

    A licence is keyed by its plans *and* its seat: the same plan is a different claim when one
    capability needs the tenant to have bought it and another needs it assigned to the caller,
    so the two are two rows rather than one row with an ambiguous answer.
    """
    counted: Counter[tuple[tuple[str, ...], str, str]] = Counter()
    for product in document["products"].values():
        for record in product.values():
            licence = record.get("licence")
            if licence:
                counted[(tuple(licence["plans"]), licence["seat"], area_of(record["type"]))] += 1
    areas: dict[tuple[tuple[str, ...], str], list[Family]] = defaultdict(list)
    for (plans, seat, area), nouns in counted.items():
        areas[(plans, seat)].append(Family(area, nouns, plans, seat))
    licences = [
        Licence(plans=plans, seat=seat, families=tuple(sorted(found, key=lambda item: (-item.nouns, item.name))))
        for (plans, seat), found in areas.items()
    ]
    return tuple(sorted(licences, key=lambda item: (-item.nouns, item.name)))


def area_of(ref: str) -> str:
    """``office365.intune.devices.management.managed.device:ManagedDevice`` -> ``intune.devices``."""
    module = ref.split(":", 1)[0]
    return ".".join(module.split(".")[1 : 1 + FAMILY_DEPTH])


def rows(licences: Iterable[Licence], held: Iterable[str], mine: Iterable[str] | None = None) -> list[dict[str, Any]]:
    """One record per licence, ready for :func:`office365.runtime.render.render`.

    Args:
        held: The plan names the tenant's subscriptions provision.
        mine: The plan names assigned to the calling identity, or ``None`` when that read was
            not made or failed - a seat is then ``unknown``, which is the honest answer and not
            a refusal.
    """
    tenant, assigned = frozenset(held), None if mine is None else frozenset(mine)
    records = [
        {
            "plan": licence.name,
            "seat": licence.seat,
            "held": _held(licence, tenant, assigned),
            "nouns": licence.nouns,
            "families": _where(licence.families),
        }
        for licence in licences
    ]
    # What the tenant can use comes first; a sort that is stable on ``of()``'s order, so the
    # licence opening the most words still leads inside each half.
    records.sort(key=lambda record: record["held"] != YES)
    return records


def headline(records: Iterable[Mapping[str, Any]], tenant: str = "") -> str:
    """One sentence: how much of what a command names this tenant can actually use."""
    answers = [row["held"] for row in records]
    total, held = len(answers), answers.count(YES)
    licence = "licence" if total == 1 else "licences"
    return f"{tenant + ': ' if tenant else ''}holds {held} of the {total} {licence} a command names"


def _held(licence: Licence, tenant: frozenset[str], assigned: frozenset[str] | None) -> str:
    """Whether this licence is held, asked of the read the seat names.

    A licence is held when *any one* of its plans is: the marker's own reading, so this is
    ``isdisjoint`` rather than a subset check.
    """
    if licence.seat != USER:
        return NO if tenant.isdisjoint(licence.plans) else YES
    if assigned is None:
        return UNKNOWN
    return NO if assigned.isdisjoint(licence.plans) else YES


def _where(families: Iterable[Family]) -> str:
    """The areas one licence opens, widest first, with a count only where it says something."""
    return ", ".join(f"{family.name} ({family.nouns})" if family.nouns > 1 else family.name for family in families)
