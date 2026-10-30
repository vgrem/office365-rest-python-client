"""A dataclass field default must be hashable, on whichever interpreter runs the tests.

Python 3.11 rejects an unhashable *instance* used as a field default::

    ValueError: mutable default <class 'mappingproxy'> for field properties is not
    allowed: use default_factory

3.12 relaxed the check back to ``list``/``dict``/``set``, so a ``mappingproxy`` default
written in a class body is legal on 3.10, 3.12, 3.13 and 3.14 and a hard import error
on 3.11 -- which is how :mod:`office365.runtime.schema` became unimportable there, and
with it every model.

Asking the interpreter "would 3.11 accept this?" is not portable, because the answer
lives in a version-specific check (``f.default.__class__.__hash__ is None`` on 3.11 and
a call-through that raises on 3.14). Asking "is this default hashable?" is: unhashable
is what 3.11 treats as mutable, on every version.
"""

from __future__ import annotations

import dataclasses
import importlib
import pkgutil
from typing import Iterator, List

import office365.runtime as runtime_package


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
