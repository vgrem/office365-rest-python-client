"""Two ratchets that walk the whole package and fail on *this* tree.

The first is ``Compare`` rules: each must say something its field's type can bear
(see ``runtime/compare_check.py``). The second is a dataclass field default: it
must be hashable on whichever interpreter runs the suite.
"""

from __future__ import annotations

import dataclasses
import importlib
import pkgutil
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Iterator, List, Optional

import office365
import office365.runtime as runtime_package
from office365.runtime.client_object import ClientObject
from office365.runtime.client_value import ClientValue
from office365.runtime.compare_check import _fields, compare_problems
from office365.runtime.types.odata_property import odata


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
    @dataclass
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
        for value in vars(module).values():
            if isinstance(value, type) and dataclasses.is_dataclass(value):
                yield value


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
