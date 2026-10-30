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


def test_no_getter_hides_the_enum_its_annotation_names() -> None:
    """The codemod plans nothing left to hoist, so no getter spells a type out of reach.

    Scoped to enums: a complex value already hydrates through the ``default_factory``
    instance the getter passes in, so its lazy import is a typing gap rather than a
    value defect and is hoisted separately.
    """
    planned = {
        str(path.relative_to(_REPO_ROOT)): [f"{site.class_name}.{site.getter} imports {site.name}" for site in sites]
        for path in sorted((_REPO_ROOT / "office365").rglob("*.py"))
        if (sites := _hoist.plan_module(path, {"enum"})[0])
    }
    assert planned == {}


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

    ``12,188`` columns resolve today; the ones that do not yet are the value-type
    imports still waiting for the same hoist, and a getter no annotation was ever
    written for. As those are finished this test starts covering them: the count it
    observes is not pinned, the agreement is.
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
