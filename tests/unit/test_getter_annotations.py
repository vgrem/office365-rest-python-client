"""A getter's annotation must be reachable where the runtime reads it.

``declared_type`` decides how to coerce a wire value by evaluating the getter's return
annotation against the module's globals. A generated getter used to spell that type
somewhere the runtime cannot see -- a function-local import, plus an ``if
TYPE_CHECKING:`` entry that never executes -- so ``get_type_hints`` raised ``NameError``
and ``declared_type`` answered ``None``. An enum column then kept the wire string:
``set_property("sourceEnvironment", "2")`` gave ``'2'`` where the metadata says
``BrowserSharedCookieSourceEnvironment.both``.

``scripts/hoist_imports.py`` moved those imports to the module block, where the
generator's own rule always said they belonged (``needs_runtime_import``: an enum
default is evaluated when the class is built). These tests hold the result closed, and
like the OData ratchet they hold it by running the codemod rather than restating its
rule -- a gate that re-spelled the rule would agree with itself.
"""

from __future__ import annotations

import datetime
import functools
import importlib
import importlib.util
import pathlib
import pkgutil
import typing

import pytest
from office365.admin.browser_shared_cookie import BrowserSharedCookie
from office365.intune.browser.sharedcookiesourceenvironment import BrowserSharedCookieSourceEnvironment
from office365.onedrive.operations.long_running import LongRunningOperation
from office365.onedrive.operations.longrunningoperationstatus import LongRunningOperationStatus
from office365.runtime.client_object import ClientObject
from office365.runtime.converters.value import declared_type
from office365.sharepoint.listitems.listitem import ListItem

_REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]

_spec = importlib.util.spec_from_file_location("_hoist_imports", _REPO_ROOT / "scripts" / "hoist_imports.py")
assert _spec is not None and _spec.loader is not None
_hoist = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_hoist)


def _service_roots() -> list[str]:
    """Every package under ``office365``, derived from the tree so none is forgotten."""
    return [
        f"office365/{entry.name}"
        for entry in sorted((_REPO_ROOT / "office365").iterdir())
        if entry.is_dir() and entry.name != "__pycache__"
    ]


def test_the_ratchet_covers_every_package_under_office365() -> None:
    covered = {pathlib.Path(root).name for root in _service_roots()}
    packages = {entry.name for entry in (_REPO_ROOT / "office365").iterdir() if entry.is_dir()}
    assert packages - covered == {"__pycache__"}


@functools.lru_cache(maxsize=1)
def _hoist_plan() -> tuple[tuple[tuple[str, tuple[str, ...]], ...], frozenset[str]]:
    """What the codemod would still move, and what it refuses to move.

    Mirrors the codemod's own loop, cycle gate included, so the test measures what
    the tool would actually write rather than what a re-spelling of its rule says.
    """
    graph = _hoist.import_graph()
    planned: dict[str, list[str]] = {}
    refused: set[str] = set()
    for path in sorted((_REPO_ROOT / "office365").rglob("*.py")):
        candidates, _ = _hoist.plan_module(path, set(_hoist.KINDS))
        sites = [site for site in candidates if not _hoist.closes_a_cycle(graph, site.target, site.module)]
        refused.update(
            f"{site.class_name}.{site.getter} imports {site.name}" for site in candidates if site not in sites
        )
        if sites:
            planned[str(path.relative_to(_REPO_ROOT))] = [
                f"{site.class_name}.{site.getter} imports {site.name}" for site in sites
            ]
        for site in sites:
            graph.setdefault(site.module, set()).add(site.target)
    return tuple((name, tuple(reasons)) for name, reasons in planned.items()), frozenset(refused)


def test_no_getter_hides_the_type_its_annotation_names() -> None:
    """The codemod plans nothing left, so no getter spells its type out of reach.

    The names it *declines* to move are mostly redundant -- the module already binds
    the same name, so the annotation resolves without the local copy -- and two are
    pinned by the next test.
    """
    planned, _ = _hoist_plan()
    assert planned == ()


def test_the_only_hoists_left_are_the_two_that_would_close_a_cycle() -> None:
    """A type both directions need stays lazy, and is named rather than dropped.

    ``ChatInfo`` and ``ConditionalAccessGrantControls`` are ``EntityCollection``
    types their owning entity imports; the answer is a runtime fallback for the
    getter, not an import neither module can have.
    """
    _, refused = _hoist_plan()
    assert refused == frozenset(
        {
            "OnlineMeetingBase.chat_info imports ChatInfo",
            "ConditionalAccessPolicy.grant_controls imports ConditionalAccessGrantControls",
        }
    )


def _modules(root: str) -> typing.Iterator[typing.Any]:
    prefix = root.replace("/", ".") + "."
    for info in pkgutil.walk_packages([str(_REPO_ROOT / root)], prefix=prefix):
        yield importlib.import_module(info.name)


def _client_objects(module: typing.Any) -> typing.Iterator[type]:
    for member in vars(module).values():
        if isinstance(member, type) and issubclass(member, ClientObject) and member.__module__ == module.__name__:
            yield member


def _getter(cls: type, name: str) -> typing.Optional[typing.Any]:
    """The property function behind a column, by the attribute its schema maps to."""
    schema = getattr(cls, "_schema", None)
    meta = schema.properties.get(name) if schema is not None else None
    member = getattr(cls, meta.attr if meta is not None else name, None)
    return member.fget if isinstance(member, property) else None


def _unwrap_optional(annotation: typing.Any) -> typing.Any:
    """``Optional[X]`` is ``X`` for a declared type: ``None`` is a nullability fact."""
    if typing.get_origin(annotation) is typing.Union:
        present = [arg for arg in typing.get_args(annotation) if arg is not type(None)]
        if len(present) == 1:
            return present[0]
    return annotation


@pytest.mark.parametrize("root", _service_roots())
def test_where_an_annotation_resolves_it_is_the_declared_type(root: str) -> None:
    """A column's declaration is the type its own getter names, across the whole tree.

    Every column resolves today; the count it observes is not pinned, the agreement
    is. A getter that states nothing is the next test's subject.
    """
    mismatches: list[str] = []
    for module in _modules(root):
        for cls in _client_objects(module):
            for name in cls.select_all():
                getter = _getter(cls, name)
                if getter is None:
                    continue
                try:
                    hints = typing.get_type_hints(getter)
                except NameError:
                    continue  # the annotation still names a type out of reach
                hint = hints.get("return")
                if hint in (None, type(None)):
                    continue
                declared = declared_type(cls, name)
                expected = _unwrap_optional(hint)
                if declared != expected:
                    mismatches.append(f"{module.__name__}.{cls.__name__}.{name}: {expected!r} declared {declared!r}")
    assert mismatches == []


@pytest.mark.parametrize("root", _service_roots())
def test_every_column_states_the_type_it_holds(root: str) -> None:
    """A column whose getter states no type is a column the runtime cannot coerce.

    ``coerce_records`` drops it as an unknown column, ``set_property`` stores the wire
    value verbatim, and a value column arrives as the dict the service sent -- the
    defects the annotation slices fixed one kind at a time. What was left after them
    was 120 hand-written getters that named their type only in the value they passed
    to ``properties.get``: ``Call.call_routes`` defaulted to
    ``ClientValueCollection(CallRoute)``, so ``callRoutes`` was skipped as unknown.
    Stating the type in the signature is what makes it a declaration, so this ratchet
    holds every column to having one -- no list of 120 to forget to extend.
    """
    silent: list[str] = []
    for module in _modules(root):
        for cls in _client_objects(module):
            for name in cls.select_all():
                if declared_type(cls, name) is None:
                    silent.append(f"{module.__name__}: {cls.__name__} reads '{name}' and states no type")
    assert silent == []


def test_a_name_only_the_type_checking_block_binds_is_hoisted(tmp_path: pathlib.Path, monkeypatch) -> None:
    """``Optional`` in ``if TYPE_CHECKING:`` never binds, so the annotation cannot resolve.
    The getter states no import of its own to move; the repair is the block's import,
    written once at module level and dropped where it was.
    """
    monkeypatch.setattr(_hoist, "_ROOT", tmp_path)
    module = tmp_path / "model.py"
    module.write_text(
        "from __future__ import annotations\n"
        "\n"
        "from typing import TYPE_CHECKING\n"
        "\n"
        "if TYPE_CHECKING:\n"
        "    from typing import Optional\n"
        "\n"
        "\n"
        "class Model:\n"
        "    @property\n"
        "    def created(self) -> Optional[str]:\n"
        "        return None\n"
    )
    sites, skipped = _hoist.plan_module(module, set(_hoist.KINDS))
    assert [(site.name, site.source) for site in sites] == [("Optional", "type_checking")]
    assert skipped == []
    _hoist.apply(module, sites)
    text = module.read_text()
    assert "from typing import Optional\n" in text.split("class Model")[0]
    assert "if TYPE_CHECKING" not in text


def test_a_stdlib_name_the_annotation_spells_is_a_declared_type() -> None:
    # ``ListItem.created`` answered ``None`` with ``NameError: name 'Optional' is not
    # defined`` -- the name sat in the module's dead ``if TYPE_CHECKING:`` block.
    assert declared_type(ListItem, "Created") is datetime.datetime
    assert declared_type(ListItem, "Modified") is datetime.datetime


def test_an_enum_column_holds_the_member_not_the_wire_string() -> None:
    # The defect in one place: the metadata spells the ordinal ("2"), and ``both`` is
    # the member it names. It stayed a string only because the type was unreachable.
    # No client: this is a value-level fact, and the model builds without one.
    cookie = BrowserSharedCookie(None)
    cookie.set_property("sourceEnvironment", "2")
    assert cookie.source_environment is BrowserSharedCookieSourceEnvironment.both
    assert declared_type(BrowserSharedCookie, "sourceEnvironment") is BrowserSharedCookieSourceEnvironment


def test_an_unfamiliar_enum_value_is_kept_as_the_service_sent_it() -> None:
    # A member the snapshot does not list (the engine's "completed", where the entity
    # enum says "succeeded") must not be coerced to None: the next update would write
    # null back over a value the service reported.
    operation = LongRunningOperation(None)
    operation.set_property("status", "completed")
    assert operation.properties["status"] == "completed"
    operation.set_property("status", "succeeded")
    assert operation.status is LongRunningOperationStatus.succeeded
