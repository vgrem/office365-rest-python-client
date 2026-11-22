"""Whole-tree invariants: a model's declarations, and the schema it answers with, agree.

These are walks, not counts. Each one asks a question of every model the package defines and
fails on this tree; none pins a number, because a number says how much is unexamined rather
than what is wrong. A count of undeclared columns, or of the files that spell column names by
hand, measures the ledger-keeper's diligence and is maintained as a date-stamped table — the
permission and fidelity audits answer the same question from the metadata itself.
"""

from __future__ import annotations

import dataclasses
import importlib
import pkgutil
from dataclasses import replace
from typing import Dict, Iterator, List

import office365
import office365.runtime as runtime_package
from office365.runtime.client_object import ClientObject
from office365.runtime.client_value import ClientValue
from office365.runtime.compare_check import _fields, compare_problems
from office365.runtime.schema import TypeSchema


def _package_models() -> list:
    """Every model the package defines, imported: the hand-written ones and the generated ones."""
    found: Dict[type, None] = {}
    for module in pkgutil.walk_packages(office365.__path__, "office365."):
        for member in vars(importlib.import_module(module.name)).values():
            if isinstance(member, type) and issubclass(member, (ClientObject, ClientValue)):
                found[member] = None
    return list(found)


def test_every_compare_rule_in_the_package_fits_its_field():
    # Three models declare these rules by hand today; naming them would let the fourth
    # escape, so the walk is the gate and a rule is found by the declaration itself.
    declaring = [model for model in _package_models() if any(meta.compare for _, meta, _ in _fields(model))]
    assert declaring, "the walk found no declaring model, so it proves nothing"
    assert [problem for model in declaring for problem in compare_problems(model)] == []


def _projection_problems(model: type) -> List[str]:
    """Every way the schema of ``model`` contradicts its own declarations.

    Each projection is one filtered line over ``properties``, so the checks below are
    the properties that filtering assumes: a member is projected one way or the other,
    a flag narrows a projection instead of widening it, and the index answers with the
    declaration it was built from.
    """
    schema = TypeSchema.of(model)
    columns, navigations = set(schema.columns), set(schema.navigations)
    readonly, persistable = set(schema.readonly), set(schema.persistable)
    problems: List[str] = []
    if columns & navigations:
        problems.append(f"$select and $expand both offer {sorted(columns & navigations)}")
    if not set(schema.expansions) <= navigations:
        problems.append(f"expandable but not a navigation: {sorted(set(schema.expansions) - navigations)}")
    if readonly & persistable:
        problems.append(f"read-only and persistable at once: {sorted(readonly & persistable)}")
    for facet, names in schema.facets.items():
        if not set(names) <= columns:
            problems.append(f"facet {facet} offers {sorted(set(names) - columns)}, which $select cannot name")
    for attr, name in schema.by_attr.items():
        if schema.properties.get(name) is None or schema.properties[name].attr != attr:
            problems.append(f"{attr} is indexed as {name}, which no declaration owns")
    return problems


def test_every_model_keeps_its_projections_coherent() -> None:
    # The migration layer reads these instead of keeping name lists of its own, so a
    # name offered twice (or a flag with no member to narrow) has to fail here rather
    # than at the `$select` the caller builds from it.
    problems = [f"{model.__name__}: {problem}" for model in _package_models() for problem in _projection_problems(model)]
    assert problems == []


def test_the_walk_reaches_models_with_both_kinds_of_member() -> None:
    # The rule above proves nothing unless the walk reaches models that project both, and
    # the projections mean nothing unless they are populated: one test states both facts.
    projecting = {m.__name__ for m in _package_models() if TypeSchema.of(m).columns and TypeSchema.of(m).navigations}
    assert {"ListItem", "Web", "Event"} <= projecting


def test_every_model_stores_the_schema_its_declarations_describe() -> None:
    # ``TypeSchema.of`` answers from the schema the class stored, never by scanning it
    # again, so a class that declares something and stores nothing answers every question
    # about itself with the empty schema -- silently, and in the direction of asking for
    # less than the model can carry. Only one thing can cause that now that
    # ``ClientValue.__init_subclass__`` reads every class: a subclass that writes its own
    # ``__init_subclass__`` and forgets ``super()``, a one-line mistake with no symptom.
    stale = [
        f"{model.__module__}.{model.__qualname__}"
        for model in _package_models()
        if replace(TypeSchema.of(model), name=model.__name__) != TypeSchema.build(model)
    ]
    assert stale == []


def _dataclasses_under(package: object) -> Iterator[type]:
    """Every dataclass defined by ``package`` and its submodules."""
    for module_info in pkgutil.walk_packages(package.__path__, package.__name__ + "."):  # type: ignore[attr-defined]
        for member in vars(importlib.import_module(module_info.name)).values():
            if isinstance(member, type) and dataclasses.is_dataclass(member):
                yield member


def _unhashable_defaults(model: type) -> List[str]:
    """The fields of ``model`` whose default is an unhashable instance."""
    offenders: List[str] = []
    for declared in dataclasses.fields(model):
        if declared.default is dataclasses.MISSING or declared.default_factory is not dataclasses.MISSING:
            continue
        try:
            hash(declared.default)
        except TypeError:
            offenders.append(declared.name)
    return offenders


def test_no_runtime_dataclass_default_is_an_unhashable_instance() -> None:
    offenders = {
        f"{model.__module__}.{model.__qualname__}.{name}": "field(default_factory=...)"
        for model in _dataclasses_under(runtime_package)
        for name in _unhashable_defaults(model)
    }
    assert not offenders, (
        "these dataclass fields default to an unhashable instance, which Python 3.11 "
        f"rejects at class-creation time: {sorted(offenders)}"
    )
