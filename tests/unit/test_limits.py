"""The limit table: the rows that publish it, the guards that enforce it, and the bindings that reach it.

A row is data a caller reads before sending a request - a value, a unit, a scope, a window, and
the page it came from - so a malformed one is a wrong budget handed to a person who cannot check
it against the code. And a row reaches a caller only through the type that spends it: the rows are
registered under a product, not on the class, and ``limits_of`` reads the class.
"""

from __future__ import annotations

import subprocess
import sys
import warnings

import pytest
from office365.directory.invitations.invitation import Invitation
from office365.directory.policies.conditionalaccess.conditional_access import ConditionalAccessPolicy
from office365.onedrive.driveitems.driveItem import DriveItem
from office365.onedrive.drives.drive import Drive
from office365.onedrive.permissions.permission import Permission
from office365.onenote.pages.page import OnenotePage
from office365.outlook.calendar.calendar import Calendar
from office365.outlook.mail.folders.folder import MailFolder
from office365.runtime.client_object import ClientObject
from office365.runtime.limits import (
    Limit,
    LimitExceededError,
    LimitKind,
    bounded,
    catalog,
    catalog_products,
    ensure_within,
    limit,
    limits_of,
    verify_limits,
    warn_if_exceeds,
)
from office365.runtime.schema import TypeSchema
from office365.runtime.types.odata_property import odata
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.thresholds import LIST_VIEW_THRESHOLD, Limits
from office365.subscriptions.collection import SubscriptionCollection
from office365.subscriptions.subscription import Subscription
from office365.teams.chats.messages.message import ChatMessage
from tests import test_site_url

LIST_VIEW = Limits.LIST_VIEW

#: What a row may say about the shape of the request it counts.
REQUEST_TYPES = {"", "read", "write", "delete", "any"}

#: The resources a migration reads most, one per spending hierarchy.
SPENDING_TYPES = (
    DriveItem,  # and everything else on ``BaseItem``
    Drive,
    Permission,
    ChatMessage,
    MailFolder,
    Calendar,
    Subscription,
    SubscriptionCollection,
    OnenotePage,
    Invitation,
    ConditionalAccessPolicy,
)


def test_every_published_row_is_well_formed():
    rows = catalog()
    assert rows, "no rows registered - the catalogs registered nothing at all"
    assert "graph" in catalog_products(), "the Graph-wide row is the one every request spends"
    for row in rows:
        assert row.name
        assert isinstance(row.kind, LimitKind)
        assert row.value > 0
        assert row.unit, f"{row.name!r} counts an unnamed unit"
        assert row.request_type in REQUEST_TYPES
        assert (row.window_seconds or 0) >= 0
        assert row.doc.startswith("https://"), f"{row.name!r} cites {row.doc!r}"


def test_one_import_exposes_every_catalog():
    """Discovery must not depend on which module a caller happened to touch first.

    A product catalog registers itself when imported, so the aggregator has to import all of
    them; a new ``quotas`` module that nobody adds there would answer ``[]`` for its product
    and vanish from the generated docs without failing anything.
    """
    code = """
import importlib, pkgutil
import office365
from office365.limits import catalog_products

seen = set(catalog_products())
for module in pkgutil.walk_packages(office365.__path__, "office365."):
    if module.name.endswith((".quotas", ".thresholds")):
        importlib.import_module(module.name)
print(sorted(set(catalog_products()) - seen - {"model"}))  # "model" is written by @limit on a class
"""
    result = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, check=True)

    assert result.stdout.strip() == "[]", f"not imported by office365/limits.py: {result.stdout.strip()}"


@pytest.mark.parametrize("target", SPENDING_TYPES, ids=lambda target: target.__name__)
def test_a_type_answers_the_published_rows_it_spends(target):
    declared = limits_of(target)
    assert declared, f"{target.__name__} declares no limits"
    published = catalog()
    for decl in declared:
        assert decl.limit in published, f"{target.__name__} declares a row no catalog published"


def test_str_formats_items_and_bytes():
    assert str(LIST_VIEW) == "5,000 items"
    assert str(Limits.FILE_UPLOAD) == "250 GB"
    assert str(Limits.LIST_ROW_BYTES) == "8,000 bytes"
    # A byte budget inside a window is bytes, not a count: readable however it is spent.
    assert str(Limit("upload", 150 * 1024 * 1024, LimitKind.SUPPORTED, "bytes", window_seconds=300)) == "150 MB / 300s"
    # A whole-day allocation stated in seconds reads like a per-second rate.
    assert str(Limit("queries", 200, LimitKind.THRESHOLD, "requests", window_seconds=86_400)) == "200 requests / 24h"
    assert str(Limit("upload", 100 * 1024**3, LimitKind.THRESHOLD, "bytes", window_seconds=3600)) == "100 GB / 1h"


def test_warn_if_exceeds():
    with pytest.warns(UserWarning, match="list view threshold"):
        assert warn_if_exceeds(LIST_VIEW, 6000) is True
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        assert warn_if_exceeds(LIST_VIEW, 10) is False


@pytest.mark.parametrize("offset", [-1, 0])
def test_the_guard_accepts_values_at_or_below_the_boundary(offset):
    value = LIST_VIEW.value + offset
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        assert not warn_if_exceeds(LIST_VIEW, value)
        ensure_within(LIST_VIEW, value)


def test_the_guard_rejects_the_first_value_above_the_boundary():
    value = LIST_VIEW.value + 1
    with pytest.warns(UserWarning, match="list view threshold"):
        assert warn_if_exceeds(LIST_VIEW, value)
    with pytest.raises(LimitExceededError) as error:
        ensure_within(LIST_VIEW, value)
    assert error.value.value == value


def test_ensure_within_raises_by_default():
    with pytest.raises(LimitExceededError) as exc:
        ensure_within(LIST_VIEW, 9000, context="query")
    assert exc.value.limit is LIST_VIEW
    assert exc.value.value == 9000  # noqa: PLR2004
    assert "query" in str(exc.value)


def test_ensure_within_warn_mode_and_passthrough():
    with pytest.warns(UserWarning):
        ensure_within(LIST_VIEW, 9000, on_exceed="warn")
    ensure_within(LIST_VIEW, 10)  # under the limit -> no raise
    with pytest.raises(ValueError, match="on_exceed"):
        ensure_within(LIST_VIEW, 10, on_exceed="nope")


def test_bounded_warns_by_default():
    @bounded("page_size", LIST_VIEW)
    def get_items(caml_query=None, page_size=None):
        return page_size

    with pytest.warns(UserWarning):
        assert get_items(page_size=6000) == 6000  # noqa: PLR2004
    assert get_items(page_size=2000) == 2000  # noqa: PLR2004
    assert get_items() is None  # None passes


def test_list_get_items_warns_when_page_size_over_threshold():
    lst = ClientContext(test_site_url).web.lists.get_by_title("X")
    with pytest.warns(UserWarning, match="list view threshold"):
        lst.get_items(page_size=LIST_VIEW_THRESHOLD + 1)


def test_limit_decorator_stamps_metadata_and_doc():
    @limit(Limits.FILE_UPLOAD)
    def upload(content):
        """Upload a file."""
        return content

    decls = limits_of(upload)
    assert len(decls) == 1
    assert decls[0].limit is Limits.FILE_UPLOAD
    assert decls[0].arg is None
    assert "Limits:" in upload.__doc__
    assert "file upload" in upload.__doc__


def test_limit_decorator_raise_and_clamp():
    @limit(Limits.LIST_VIEW, arg="page_size", on_exceed="raise")
    def strict(page_size=None):
        return page_size

    with pytest.raises(LimitExceededError):
        strict(page_size=6000)

    @limit(Limits.LIST_VIEW, arg="page_size", clamp=True)
    def clamped(page_size=None):
        return page_size

    assert clamped(page_size=6000) == Limits.LIST_VIEW.value


def test_limits_are_one_of_the_things_a_type_declares():
    """A class's limits and its slots are the same kind of fact, so they live together.

    ``limits_of()``, ``declared_limits()`` and the inheritance a subclass needs all read the one
    object the class built, and a context declares limits through the same field a model declares
    properties through.
    """

    @limit(Limits.LIST_VIEW)
    class _Tier(ClientObject):
        @limit(Limits.FILE_UPLOAD)
        @property
        def upload(self):
            return None

        @limit(Limits.BATCH_ITEMS, arg="page_size")
        def get_items(self, page_size=None):
            return page_size

    class _Child(_Tier):
        pass

    assert [decl.limit for decl in _Tier._schema.class_limits] == [Limits.LIST_VIEW]
    assert set(_Tier._schema.member_limits) == {"upload", "get_items"}
    assert _Tier.declared_limits() == (Limits.LIST_VIEW, Limits.FILE_UPLOAD, Limits.BATCH_ITEMS)
    # The type's own row comes first: a class is subject to what it declares on itself.
    assert [decl.limit for decl in limits_of(_Tier)] == [Limits.LIST_VIEW, Limits.FILE_UPLOAD, Limits.BATCH_ITEMS]
    assert _Child._schema.class_limits == _Tier._schema.class_limits  # inherited, not shared map
    assert _Child._schema is not _Tier._schema
    assert Limits.LIST_VIEW in _Child.declared_limits()
    # A context declares no properties, and still declares limits.
    assert ClientContext._schema.properties == {}
    assert Limits.BATCH_ITEMS in ClientContext.declared_limits()


def test_a_class_answers_its_own_rows_and_counts_each_declaration_once():
    """``limits_of(cls)`` is the declaration view of ``declared_limits()``.

    A type declares some rows on itself and some on its members; asking the class used to answer
    only the members' rows, so ``verify_limits(Workbook)`` said "0 limit(s)" for a workbook whose
    two quotas are written on the class. Two members that share a row and an argument is one
    ceiling on the type, not two.
    """

    @limit(Limits.LIST_VIEW)
    class _Tier(ClientObject):
        @limit(Limits.BATCH_ITEMS, arg="items_per_batch")
        def execute_batch(self, items_per_batch=None):
            return items_per_batch

        @limit(Limits.BATCH_ITEMS, arg="items_per_batch")
        def execute_batch_async(self, items_per_batch=None):
            return items_per_batch

    report = verify_limits(_Tier)
    assert report.limits == (Limits.LIST_VIEW, Limits.BATCH_ITEMS)
    assert [decl.limit for decl in limits_of(_Tier)] == [Limits.LIST_VIEW, Limits.BATCH_ITEMS]


def test_verify_limits_reports_violations():
    @limit(Limits.LIST_VIEW, arg="page_size")
    def get_items(page_size=None):
        return page_size

    assert verify_limits(get_items, page_size=10).ok
    report = verify_limits(get_items, page_size=6000)
    assert not report.ok
    assert "list view threshold" in str(report)


_STACK_ROWS = (
    Limit(
        "microsoft teams",
        200,
        LimitKind.SUPPORTED,
        "requests",
        "app",
        doc="https://example.com/throttling",
        window_seconds=1,
        request_type="read",
    ),
    Limit(
        "microsoft teams",
        1,
        LimitKind.SUPPORTED,
        "requests",
        "user",
        doc="https://example.com/throttling",
        window_seconds=1,
        request_type="write",
    ),
)


class _NavigationOutermost(ClientObject):
    """``@odata`` above ``@limit``: two facts, two decorators, one member."""

    @odata(name="channels", navigation=True)
    @property
    @limit(*_STACK_ROWS)
    def channels(self) -> object:
        """The channel collection."""


class _NavigationInnermost(ClientObject):
    """The other order, because nothing but ``TypeSchema`` reads a marker."""

    @limit(*_STACK_ROWS)
    @odata(name="channels", navigation=True)
    @property
    def channels(self) -> object:
        """The channel collection."""


@pytest.mark.parametrize("model", [_NavigationOutermost, _NavigationInnermost], ids=lambda m: m.__name__)
def test_a_member_is_a_navigation_and_a_budgeted_call_at_once(model):
    """``@odata`` answers representation, ``@limit`` answers budget: they do not overlap.

    Stacking them is what binds a Teams endpoint's budgets to the member that names it, and the
    order must not matter: neither decorator reads the other's marker.
    """
    declared = model._schema.properties["channels"]
    assert declared.navigation is True
    assert "channels" not in model._schema.columns
    assert TypeSchema.of(model).columns == ()
    assert TypeSchema.of(model).expansions == ("channels",)
    assert [decl.limit for decl in limits_of(model)] == list(_STACK_ROWS)
    # The section is written on the getter. In one order ``property`` copies that doc, in the
    # other it has already copied it -- so read the declaration, not the copy.
    doc = model.__dict__["channels"].fget.__doc__
    assert doc.count("Limits:") == 1
    assert [line.strip() for line in doc.splitlines() if line.startswith("      ")] == [
        "microsoft teams (read on app): 200 requests / 1s",
        "microsoft teams (write on user): 1 request / 1s",
    ]
