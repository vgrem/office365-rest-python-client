"""A system column is read through its field, not spelled out again by name.

``ListItem`` declares six *system* columns — an item row carries them even though the v3
CSDL does not — and their getters are plain bag reads, so ``item.created`` and
``item.properties.get("Created")`` return the very same value. What separates them is that
the field says which column it is: a literal turns a rename in the model into a silent
``None``, and an empty column reads exactly like "no value".

The rule is about the *shape*, not about the string: projection lists (``select([...])``)
and payload keys are wire names by nature and keep spelling them, while a read of a
``properties`` bag — directly or through a local alias — goes through the field. The set is
derived from ``ListItem._schema.system`` so the declaration stays the owner; the six are
pinned because an empty ``system`` mapping would otherwise turn the guard into a no-op.
"""

from __future__ import annotations

import ast
import pathlib
from typing import Iterator, Tuple

from office365.sharepoint.listitems.listitem import ListItem


def _bag_reads(source: str) -> Iterator[Tuple[int, str]]:
    """Every ``properties.get("...")`` read in ``source``, alias form included."""
    tree = ast.parse(source)
    scopes = [tree, *(node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef))]
    seen = set()
    for scope in scopes:
        aliases = {
            target.id
            for node in ast.walk(scope)
            if isinstance(node, ast.Assign)
            for target in node.targets
            if isinstance(target, ast.Name) and isinstance(node.value, ast.Attribute) and node.value.attr == "properties"
        }
        for node in ast.walk(scope):
            if not (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)):
                continue
            if node.func.attr != "get" or not node.args:
                continue
            receiver = node.func.value
            is_bag = (isinstance(receiver, ast.Attribute) and receiver.attr == "properties") or (
                isinstance(receiver, ast.Name) and receiver.id in aliases
            )
            name = node.args[0]
            if is_bag and isinstance(name, ast.Constant) and isinstance(name.value, str):
                spot = (node.lineno, name.value)
                if spot not in seen:
                    seen.add(spot)
                    yield spot


def _declared_system_columns() -> frozenset:
    """The item columns the model declares as system members."""
    return frozenset(ListItem._schema.system)


def test_the_layer_reads_a_system_column_through_its_field() -> None:
    from office365.migration.sharepoint import __path__ as package

    forbidden = _declared_system_columns()
    assert forbidden == {"AuthorId", "EditorId", "Created", "Modified", "FileLeafRef", "FileRef"}, (
        "ListItem._schema.system changed: it owns these spellings, so a new system column "
        "belongs here (and the layer reads it through its field)"
    )
    field_of = {wire: attr for attr, wire in ListItem._schema.by_attr.items()}
    offenders = {
        f"{path.relative_to(package[0])}:{line}": f"properties.get({name!r}) -> .{field_of[name]}"
        for path in sorted(pathlib.Path(package[0]).rglob("*.py"))
        for line, name in _bag_reads(path.read_text(encoding="utf-8"))
        if name in forbidden
    }
    assert not offenders, f"read these through the field instead: {sorted(offenders.items())}"


def test_the_ratchet_sees_the_construct_it_forbids() -> None:
    forbidden = _declared_system_columns()
    direct = 'def f(item):\n    return item.properties.get("Created")\n'
    aliased = 'def f(item):\n    bag = item.properties\n    return bag.get("AuthorId")\n'
    raw_dict = 'def f(record):\n    return record.get("Created")\n'
    wired = "def f(item):\n    return item.created\n"
    assert [name for _, name in _bag_reads(direct) if name in forbidden] == ["Created"]
    assert [name for _, name in _bag_reads(aliased) if name in forbidden] == ["AuthorId"]
    assert [name for _, name in _bag_reads(raw_dict) if name in forbidden] == []
    assert list(_bag_reads(wired)) == []
