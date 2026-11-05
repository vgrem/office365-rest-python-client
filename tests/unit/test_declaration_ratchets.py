"""Five ratchets that walk the whole package and fail on *this* tree.

The first is ``Compare`` rules: each must say something its field's type can bear
(see ``runtime/compare_check.py``). The second is a dataclass field default: it
must be hashable on whichever interpreter runs the suite. The third is the set of
projections ``TypeSchema`` derives: a caller that asks the model instead of keeping
its own name list is only served if the projections stay a partition of what the
declarations say. The fourth is the schema a model stores: it is only an answer if
it is the one its declarations describe. The fifth is the write direction of a type
the migration layer creates: a column nobody has said the service owns is a name a
caller may still send, so the count of those may only fall.
"""

from __future__ import annotations

import dataclasses
import importlib
import pkgutil
from dataclasses import field, replace
from datetime import datetime
from typing import Dict, Iterator, List, Optional

import office365
import office365.runtime as runtime_package
from office365.runtime.client_object import ClientObject
from office365.runtime.client_value import ClientValue
from office365.runtime.compare_check import _fields, compare_problems
from office365.runtime.schema import TypeSchema
from office365.runtime.types.odata_property import odata
from office365.sharepoint.contenttypes.content_type import ContentType
from office365.sharepoint.fields.field import Field
from office365.sharepoint.files.file import File
from office365.sharepoint.folders.folder import Folder
from office365.sharepoint.listitems.listitem import ListItem
from office365.sharepoint.lists.list import List as SharePointList
from office365.sharepoint.principal.groups.group import Group
from office365.sharepoint.principal.users.user import User
from office365.sharepoint.publishing.pages.page import SitePage
from office365.sharepoint.webs.web import Web


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


def _problems(**declared) -> list:
    class Sample(ClientValue):
        text: Optional[str] = field(default=None, metadata=odata("text", compare=declared.get("text")))
        when: Optional[datetime] = field(default=None, metadata=odata("when", compare=declared.get("when")))
        number: Optional[int] = field(default=None, metadata=odata("number", compare=declared.get("number")))
        label: Optional[str] = field(default=None, metadata=odata("label", compare=declared.get("label")))

    return compare_problems(Sample)


def _dataclasses_under(package: object) -> Iterator[type]:
    """Every dataclass defined by ``package`` and its submodules."""
    for module_info in pkgutil.walk_packages(package.__path__, package.__name__ + "."):  # type: ignore[attr-defined]
        module = importlib.import_module(module_info.name)
        for member in vars(module).values():
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
    # again, so a class that declares something and stores nothing answers every
    # question about itself with the empty schema -- silently, and in the direction of
    # asking for less than the model can carry. Only one thing can still cause that now
    # that ``ClientValue.__init_subclass__`` reads every class: a subclass that writes
    # its own ``__init_subclass__`` and forgets ``super()``, which is a one-line mistake
    # with no visible symptom, so the walk is the gate.
    stale = [
        f"{model.__module__}.{model.__qualname__}"
        for model in _package_models()
        if replace(TypeSchema.of(model), name=model.__name__) != TypeSchema.build(model)
    ]
    assert stale == []


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


#: The SharePoint types the migration layer creates with a POST. A create sends a handful
#: of settings into a model of a hundred columns, so most of the model is a name a caller
#: *may* send and the service answers 400 for. Where those columns are declared read-only,
#: ``to_json`` drops them and the question is closed; where they are not, the caller has to
#: know which ones those are, so the count is measured here instead of being guessed at a
#: call site.
_CREATED = (SharePointList, Web, User, Group, Field, ContentType, Folder, File, ListItem, SitePage)

#: Created types whose write direction was probed live (a ``MERGE`` per column): most of
#: their columns are declared, and extending that is a probe, not an edit -- so the pin
#: below stays off them and only the floor is held.
_PROBED = (File, Folder, ListItem, Field, ContentType, SitePage)

#: Created types whose write direction is still unconsidered: columns minus read-only
#: declarations, read off the tree on 2026-11-05. The number may only fall -- a column that
#: arrives with no direction decided fails here, which is the cheapest place to decide it.
#: List and Web are containers whose create payload is a named handful of settings, and the
#: principal types carry four flags that site security writes; the rest of each model is
#: the service's, and saying so needs the same probe the others got.
_UNDECLARED = {"List": 97, "Web": 117, "User": 16, "Group": 16}


def _undeclared(model: type) -> int:
    """The columns of ``model`` that no declaration says the service owns."""
    schema = TypeSchema.of(model)
    return len(schema.columns) - len(schema.readonly)


def test_a_created_type_says_which_columns_it_does_not_send() -> None:
    # Two ways to answer the same question -- "may I send this column?" -- and every created
    # type has to take one of them: declare the read-only columns, or be counted here. What
    # the ratchet forbids is the third case, where nobody has said anything and the answer
    # silently reads "yes" for every column the generator adds. A declared column lowers the
    # count without failing anything, so the pin is a ceiling and never a target.
    assert set(_UNDECLARED) | {model.__name__ for model in _PROBED} == {m.__name__ for m in _CREATED}
    assert [model.__name__ for model in _PROBED if not TypeSchema.of(model).readonly] == []
    grown = {
        name: undeclared
        for name, undeclared in (
            (model.__name__, _undeclared(model)) for model in _CREATED if model.__name__ in _UNDECLARED
        )
        if undeclared > _UNDECLARED[name]
    }
    assert grown == {}, f"these created types gained a column with no declared direction: {grown}"
