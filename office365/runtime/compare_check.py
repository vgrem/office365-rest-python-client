"""A lint for ``Compare`` declarations: do they say something the field's type can bear?

A rule is declared on a field and read by ``COMPARABLE`` as already-spelled JSON, so a rule
on the wrong kind of field does not fail, it silently does nothing (``unordered`` on a
string, ``format="date"`` on a number). Checking at class creation is not possible
(a ``TYPE_CHECKING``-only annotation resolves to ``None`` there), so the check is a function
a test runs over the models: :func:`compare_problems`.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Iterator, List, Optional, Set, Tuple, get_args, get_origin

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.schema import TypeSchema
from office365.runtime.types.odata_property import Compare, ODataPropertyMeta

_COLLECTION = (ClientValueCollection, list, tuple, set)
#: What each named format can be applied to.
_FORMAT_TYPES = {"date": (str, datetime), "wall-clock": (str,), "text": (str,)}


def _origin(declared: Any) -> Any:
    return get_origin(declared) or declared


def _is_collection(declared: Any) -> bool:
    origin = _origin(declared)
    return isinstance(origin, type) and issubclass(origin, _COLLECTION)


def _item_type(declared: Any) -> Any:
    args = get_args(declared)
    return args[0] if args else None


def _is_client_value(declared: Any) -> bool:
    origin = _origin(declared)
    return isinstance(origin, type) and issubclass(origin, ClientValue)


def _fields(model: type) -> Iterator[Tuple[str, ODataPropertyMeta, Any]]:
    """``(label, declaration, resolved type)`` for every declared field of ``model``."""
    for name, meta in TypeSchema.of(model).properties.items():
        if not meta.navigation:
            yield name, meta, TypeSchema.of(model).dtypes[name]


def _check(model: type, label: str, rule: Compare, declared: Any, siblings: Set[str]) -> List[str]:
    where = f"{model.__name__}.{label}"
    if declared is None:
        return [f"{where}: has a Compare rule but its type cannot be resolved, so the rule is unchecked"]
    problems: List[str] = []
    if rule.unordered and not _is_collection(declared):
        problems.append(f"{where}: unordered needs a collection, the type is {declared!r}")
    scalar = _item_type(declared) if _is_collection(declared) else declared
    scalar = str if _is_collection(declared) and scalar is None and not rule.unordered else scalar
    if rule.casefold and scalar not in (str, None):
        problems.append(f"{where}: casefold needs text, the type is {declared!r}")
    if rule.format and not (isinstance(scalar, type) and issubclass(scalar, _FORMAT_TYPES[rule.format])):
        problems.append(f"{where}: format {rule.format!r} needs one of {_FORMAT_TYPES[rule.format]}, got {declared!r}")
    if rule.fallback and rule.fallback not in siblings:
        problems.append(f"{where}: fallback {rule.fallback!r} is not a sibling field")
    if rule.ignore and (rule.key or rule.default is not None or rule.fallback):
        problems.append(f"{where}: ignore contradicts key/default/fallback (an ignored field takes no part)")
    return problems


def compare_problems(model: type, _seen: Optional[Set[type]] = None) -> List[str]:
    """Everything wrong with the ``Compare`` declarations of ``model`` and the value types it carries."""
    seen = _seen if _seen is not None else set()
    if model in seen:
        return []
    seen.add(model)
    fields = list(_fields(model))
    siblings = {label for label, _, _ in fields}
    problems: List[str] = []
    for label, meta, declared in fields:
        if meta.compare is not None:
            problems += _check(model, label, meta.compare, declared, siblings)
        carried = _item_type(declared) if _is_collection(declared) else declared
        if _is_client_value(carried):
            problems += compare_problems(_origin(carried), seen)
    return problems
