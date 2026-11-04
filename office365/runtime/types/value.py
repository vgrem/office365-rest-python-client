"""Declaring a client value: its fields, the facts they state, and one rendering."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Type, TypeVar

from typing_extensions import dataclass_transform

from office365.runtime.schema import TypeSchema

T = TypeVar("T")


@dataclass_transform()
def value(cls: Type[T]) -> Type[T]:
    """Declare ``cls`` as a client value.

    A value is a dataclass whose fields carry its declarations, and it renders through the
    bounded ``__repr__`` it inherits: a value may hold a whole list item's payload, so its
    rendering is truncated and cycle-safe instead of recursive.

    ``repr=False`` is that decision, stated once and to the decorator that would have
    contradicted it: no ``__repr__`` is installed, so a class that states one keeps it (a
    collection's preview) and every other class keeps the rendering its base states. The
    schema is read here because this is the first moment the class is finished -- its
    fields have their names, and no decorator above this one can still add a field.

    ``dataclass_transform`` is what tells a type checker that the decorator -- not a
    literal ``@dataclass`` above the class -- is what gives it its fields, its
    ``__init__`` and its defaults. Without it a checker sees a class with no constructor,
    which is why every library that owns this name carries the same marker.

    Args:
        cls: The class being declared.
    """
    declared: Any = dataclass(cls, repr=False)
    declared._schema = TypeSchema.build(declared)
    return declared
