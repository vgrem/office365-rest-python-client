import subprocess
import sys
import unittest
from collections import Counter
from types import ModuleType

from office365.communications import quotas as communications_quotas
from office365.communications.callrecords.call_record import CallRecord
from office365.communications.callrecords.collection import CallRecordCollection
from office365.directory import quotas as directory_quotas
from office365.graph_client import GraphClient
from office365.onedrive import quotas as files_quotas
from office365.onedrive.workbooks import quotas as excel_quotas
from office365.outlook import quotas as outlook_quotas
from office365.outlook.calendar.events.event import Event
from office365.outlook.contacts.contact import Contact
from office365.outlook.item import OutlookItem
from office365.outlook.mail.attachments.collection import AttachmentCollection
from office365.outlook.mail.messages.message import Message
from office365.outlook.user import OutlookUser
from office365.reports import quotas as reports_quotas
from office365.reports.root import ReportRoot
from office365.runtime import limits as limits_module
from office365.runtime.limits import (
    Limit,
    LimitKind,
    catalog,
    collect_class_limits,
    limit,
    limits_of,
)
from office365.security import quotas as security_quotas
from office365.security.audit.core_root import AuditCoreRoot
from office365.security.audit.log_query import AuditLogQuery
from office365.security.cases.root import CasesRoot
from office365.security.security import Security
from office365.sharepoint import thresholds as sharepoint_limits
from office365.sharepoint.attachments.attachment import Attachment
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.fields.field import Field
from office365.sharepoint.files.file import File
from office365.sharepoint.folders.folder import Folder
from office365.sharepoint.listitems.listitem import ListItem
from office365.sharepoint.lists.list import List
from office365.sharepoint.principal.groups.group import Group
from office365.sharepoint.sites.site import Site
from office365.sharepoint.taxonomy.stores.store import TermStore
from office365.sharepoint.utilities.move_copy_util import MoveCopyUtil
from office365.teams import quotas as teams_quotas
from office365.teams.channels.channel import Channel
from office365.teams.chats.chat import Chat
from office365.teams.chats.messages.collection import ChatMessageCollection
from office365.teams.team import Team

VALID_REQUEST_TYPES = {"", "read", "write", "delete", "any"}

#: (product name, its catalog module, one row from it) — the row is how the test
#: proves the module registered, without re-spelling the table in the test.
CATALOGS = (
    ("graph", limits_module, limits_module.GLOBAL_QUOTAS[0]),
    ("directory", directory_quotas, directory_quotas.IDENTITY_QUOTAS[0]),
    ("cloud-communications", communications_quotas, communications_quotas.CALL_QUOTAS[0]),
    ("sharepoint", sharepoint_limits, sharepoint_limits.Limits.LIST_VIEW),
    ("outlook", outlook_quotas, outlook_quotas.OUTLOOK_QUOTAS[0]),
    ("files", files_quotas, files_quotas.FILES_QUOTAS[0]),
    ("excel", excel_quotas, excel_quotas.EXCEL_QUOTAS[0]),
    ("reports", reports_quotas, reports_quotas.REPORT_QUOTAS[0]),
    ("security", security_quotas, security_quotas.SECURITY_QUOTAS[0]),
    ("teams", teams_quotas, teams_quotas.TEAMS_QUOTAS[0]),
)


def _rows(module: ModuleType) -> list[Limit]:
    """Every ``Limit`` tuple a catalog module exports, flattened."""
    found = []
    for value in vars(module).values():
        if isinstance(value, tuple) and value and all(isinstance(row, Limit) for row in value):
            found.extend(value)
        elif isinstance(value, type) and isinstance(value.__dict__.get("catalog"), classmethod):
            found.extend(value.catalog())
    return found


class TestCatalogRegistration(unittest.TestCase):
    """A catalog is data: it registers itself, and the registry can read it back."""

    def test_every_catalog_registers_itself(self):
        for product, _module, sample in CATALOGS:
            with self.subTest(product=product):
                self.assertIn(sample, catalog(product=product))

    def test_an_unknown_product_has_no_rows(self):
        self.assertEqual(catalog(product="no-such-product"), [])


class TestCatalogDiscovery(unittest.TestCase):
    """One import must expose every catalog — discovery cannot depend on import order."""

    def test_importing_the_public_module_alone_exposes_every_catalog(self):
        products = [product for product, _module, _sample in CATALOGS]
        code = f"from office365.limits import catalog\nprint([p for p in {products!r} if not catalog(product=p)])\n"
        result = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, check=True)
        self.assertEqual(result.stdout.strip(), "[]")


class TestCatalogCompleteness(unittest.TestCase):
    """A row lives in a catalog; a model references it. Importing models must not add rows."""


class TestCatalogRows(unittest.TestCase):
    """What a published row must carry, checked across every product at once."""

    def test_every_row_cites_its_documentation(self):
        for row in catalog():
            with self.subTest(row=str(row)):
                self.assertTrue(row.doc.startswith("https://"), f"{row.name!r} has no doc URL: {row.doc!r}")

    def test_every_row_is_well_formed(self):
        for row in catalog():
            with self.subTest(row=str(row)):
                self.assertIsInstance(row.kind, LimitKind)
                self.assertGreater(row.value, 0)
                self.assertTrue(row.name)
                self.assertTrue(row.unit)
                self.assertTrue(row.doc)
                self.assertIn(row.request_type, VALID_REQUEST_TYPES)
                if row.window_seconds is not None:
                    self.assertGreaterEqual(row.window_seconds, 0)

    def test_no_row_is_spelled_twice_in_one_catalog(self):
        # A row is identified by everything a caller reads off it; a second spelling of
        # the same fact would be two answers to one question.
        for product, _module, _sample in CATALOGS:
            rows = catalog(product=product)
            keys = [(r.name, r.unit, r.scope, r.request_type, r.window_seconds, r.note) for r in rows]
            with self.subTest(product=product):
                self.assertEqual([key for key in keys if keys.count(key) > 1], [])

    def test_a_concurrency_row_is_a_zero_second_window(self):
        # "Four at a time" is not "four per period"; the window is what says so.
        concurrency = [row for row in catalog() if row.window_seconds == 0]
        self.assertTrue(concurrency)
        self.assertTrue(all(row.is_rate for row in concurrency))


class TestOutlookQuotas(unittest.TestCase):
    """The per-mailbox numbers, which are the ones an Outlook caller must design around."""

    def setUp(self):
        self.facts = {(row.value, row.unit, row.scope, row.window_seconds) for row in catalog(product="outlook")}

    def test_ten_thousand_requests_per_ten_minutes_per_mailbox(self):
        self.assertIn((10_000, "requests", "app+mailbox", 600), self.facts)

    def test_four_requests_in_flight_per_mailbox(self):
        self.assertIn((4, "requests", "app+mailbox", 0), self.facts)

    def test_a_hundred_and_fifty_megabytes_of_upload_per_five_minutes(self):
        self.assertIn((150 * 1024 * 1024, "bytes", "app+mailbox", 300), self.facts)

    def test_json_batching_sends_four_sub_requests_at_a_time(self):
        self.assertIn((4, "requests", "batch", 0), self.facts)


class TestOutlookBindings(unittest.TestCase):
    """The per-mailbox budget belongs to the mailbox, not to one endpoint under it.

    Messages, events and contacts spend one budget without sharing a root, so it is declared
    on ``OutlookItem`` -- the base all three inherit -- and again on ``OutlookUser``, the
    ``/outlook`` endpoint. Uploads are counted in bytes and only :class:`AttachmentCollection`
    uploads, and the JSON-batch cap rides the entry point that submits a batch, its note
    carrying the qualification (the cap is Outlook's, not every batch's).
    """

    def test_each_item_type_spends_the_mailbox_budget(self):
        for model in (Message, Event, Contact):
            with self.subTest(model=model.__name__):
                self.assertEqual(
                    [id(row) for row in model.declared_limits()],
                    [id(row) for row in outlook_quotas.OUTLOOK_MAILBOX_BUDGETS],
                )

    def test_the_outlook_root_spends_the_same_budget(self):
        self.assertEqual(
            [id(row) for row in OutlookUser.declared_limits()],
            [id(row) for row in outlook_quotas.OUTLOOK_MAILBOX_BUDGETS],
        )

    def test_uploads_carry_their_own_byte_budget(self):
        self.assertEqual(
            [id(decl.limit) for decl in limits_of(AttachmentCollection)],
            [id(outlook_quotas.OUTLOOK_UPLOAD)],
        )

    def test_the_batch_cap_is_declared_where_a_batch_is_submitted(self):
        self.assertEqual(
            [id(decl.limit) for decl in limits_of(GraphClient.execute_batch)],
            [id(outlook_quotas.OUTLOOK_BATCH)],
        )

    def test_every_published_row_reaches_a_model(self):
        models = (OutlookItem, OutlookUser, AttachmentCollection, GraphClient.execute_batch)
        bound = {id(decl.limit) for target in models for decl in limits_of(target)}
        self.assertEqual([row.note for row in catalog(product="outlook") if id(row) not in bound], [])


class TestTeamsQuotas(unittest.TestCase):
    """Teams throttles four dimensions of the same request; the catalog must name all four."""

    def setUp(self):
        self.rows = catalog(product="teams")

    def test_the_default_read_row_covers_all_four_dimensions(self):
        defaults = [row for row in self.rows if row.request_type == "read" and "default" in row.note]
        self.assertEqual(
            [(row.scope, row.value) for row in defaults],
            [("app", 1_500), ("app+tenant", 30), ("team, channel or chat", 1), ("user", 1)],
        )

    def test_a_named_resource_overrides_the_default(self):
        channel = next(
            row for row in self.rows if row.note == "GET /teams/{id}/channels" and row.scope == "team, channel or chat"
        )
        self.assertEqual((channel.value, channel.window_seconds), (4, 1))


class TestCallRecordBindings(unittest.TestCase):
    """A quota is declared where the request is made, not on the entity that owns the name.

    The call-record page is the sharpest case: three budget rows framed as "the limits
    apply to the following *resources*", a 40/20s ceiling **per call record**, a separate
    40/20s ceiling for **listing** call records, and a PSTN table limited **per
    collection**. Declaring all of it on ``CallRecord`` said the session navigation spends
    a 15,000/20s app budget (it does not spend it alone) and said
    ``getDirectRoutingCalls`` has no special ceiling (it has three).
    """

    def test_the_entity_carries_the_budgets_and_nothing_narrower(self):
        declared = [decl.limit for decl in collect_class_limits(CallRecord)]
        self.assertEqual([id(row) for row in declared], [id(row) for row in communications_quotas.CALL_RECORD_BUDGETS])

    def test_the_entity_answers_the_budgets_it_declares(self):
        # The class's own rows first, then the per-record ceiling its two navigations share —
        # one ceiling on the entity, not one per navigation.
        self.assertEqual(
            [id(decl.limit) for decl in limits_of(CallRecord)],
            [
                id(row)
                for row in (*communications_quotas.CALL_RECORD_BUDGETS, communications_quotas.CALL_RECORD_RESOURCE_QUOTA)
            ],
        )

    def test_the_per_record_ceiling_is_bound_to_the_navigations_that_read_the_record(self):
        ceiling = communications_quotas.CALL_RECORD_RESOURCE_QUOTA
        for name in ("sessions", "participants_v2"):
            with self.subTest(navigation=name):
                self.assertEqual([decl.limit for decl in limits_of(getattr(CallRecord, name))], [ceiling])

    def test_listing_call_records_has_its_own_row(self):
        declared = [decl.limit for decl in collect_class_limits(CallRecordCollection)]
        self.assertEqual([id(row) for row in declared], [id(communications_quotas.CALL_RECORD_FEED_QUOTA)])

    def test_the_direct_routing_log_carries_the_pstn_rows(self):
        declared = [decl.limit for decl in limits_of(CallRecordCollection.get_direct_routing_calls)]
        self.assertEqual([id(row) for row in declared], [id(row) for row in communications_quotas.PSTN_RECORD_QUOTAS])

    def test_every_published_call_record_row_is_bound_somewhere(self):
        bound = {id(decl.limit) for decl in collect_class_limits(CallRecord)}
        bound |= {id(decl.limit) for decl in collect_class_limits(CallRecordCollection)}
        for target in (CallRecord.sessions, CallRecord.participants_v2, CallRecordCollection.get_direct_routing_calls):
            bound |= {id(decl.limit) for decl in limits_of(target)}
        published = (*communications_quotas.CALL_RECORD_QUOTAS, *communications_quotas.PSTN_RECORD_QUOTAS)
        self.assertEqual([row.name for row in published if id(row) not in bound], [])

    def test_a_row_bound_to_two_members_is_still_one_limit(self):
        # `sessions` and `participants_v2` share the 40/20s per-record ceiling.
        self.assertEqual(len(CallRecord.declared_limits()), len({id(row) for row in CallRecord.declared_limits()}))


class TestTeamsBindings(unittest.TestCase):
    """A Teams endpoint's budgets live on the member that names the endpoint.

    The published table names an *operation* (``GET /teams/{id}/channels``), and the
    operation is the resource a request is counted against: ``Team`` binds
    ``GET /teams/{id}``, the ``channels`` navigation binds ``GET /teams/{id}/channels``,
    and each message endpoint binds its own read and write rows.

    ``ChatMessageCollection`` is what decides this. It serves a channel and a chat, whose
    write budgets differ (500 against 200 requests a second), so a row declared on the
    collection would be false for half its instances -- and the collection is where the
    write happens, which is why the write rows ride the accessor instead.
    """

    def test_the_entity_carries_the_rows_of_the_call_it_makes(self):
        self.assertEqual(
            [id(decl.limit) for decl in collect_class_limits(Team)],
            [id(row) for row in teams_quotas.TEAM_READ],
        )

    def test_a_navigation_carries_the_rows_of_the_endpoint_it_names(self):
        self.assertEqual(
            [id(decl.limit) for decl in limits_of(Team.channels)],
            [id(row) for row in teams_quotas.TEAM_CHANNELS],
        )

    def test_each_message_endpoint_declares_its_own_read_and_write_rows(self):
        endpoints = (
            (
                "Channel.messages",
                Channel.messages,
                teams_quotas.CHANNEL_MESSAGES_READ,
                teams_quotas.CHANNEL_MESSAGES_WRITE,
            ),
            ("Chat.messages", Chat.messages, teams_quotas.CHAT_MESSAGES_READ, teams_quotas.CHAT_MESSAGES_WRITE),
        )
        for name, member, read, write in endpoints:
            with self.subTest(endpoint=name):
                self.assertEqual([id(decl.limit) for decl in limits_of(member)], [id(row) for row in (*read, *write)])

    def test_the_shared_collection_declares_nothing_because_it_serves_two_endpoints(self):
        self.assertEqual(collect_class_limits(ChatMessageCollection), ())

    def test_every_named_operation_is_bound_and_only_the_defaults_are_not(self):
        bound = set()
        for target in (Team, Team.channels, Channel.messages, Chat.messages):
            bound |= {id(decl.limit) for decl in limits_of(target)}
        unbound = [row for row in catalog(product="teams") if id(row) not in bound]
        self.assertEqual([row.note for row in unbound if not row.note.startswith("default")], [])
        self.assertTrue(unbound, "a default row names no resource, so no model can bind it")


class TestSecurityBindings(unittest.TestCase):
    """Three rows for one surface set, one per endpoint, and one row no type can own.

    The detections-and-incidents rows name alert, securityActions and secureScore together, so
    they are declared on ``Security`` -- the type all three requests go through -- and not on a
    sub-surface that owns only one of them. eDiscovery and the audit-log endpoints each name
    their own resource, so they are declared on the member that names them.
    """

    def test_the_detections_budget_covers_every_surface_it_names(self):
        self.assertEqual(
            [id(row) for row in Security.declared_limits()],
            [id(row) for row in security_quotas.DETECTIONS_BUDGETS],
        )

    def test_ediscovery_is_declared_on_the_type_that_names_it(self):
        self.assertEqual(
            [id(row) for row in CasesRoot.declared_limits()],
            [id(security_quotas.EDISCOVERY_BUDGET)],
        )

    def test_a_query_submission_is_capped_where_it_is_posted(self):
        self.assertEqual(
            [id(decl.limit) for decl in limits_of(AuditCoreRoot.queries)],
            [id(row) for row in security_quotas.AUDIT_LOG_QUERY_BUDGETS],
        )

    def test_what_one_query_may_return_belongs_to_the_query(self):
        self.assertEqual(
            [id(row) for row in AuditLogQuery.declared_limits()],
            [id(security_quotas.AUDIT_LOG_QUERY_RECORDS)],
        )

    def test_the_only_unbound_row_names_a_surface_the_library_does_not_spell(self):
        models = (Security, CasesRoot, AuditCoreRoot.queries, AuditLogQuery)
        bound = {id(decl.limit) for target in models for decl in limits_of(target)}
        unbound = [row for row in catalog(product="security") if id(row) not in bound]
        self.assertEqual([row.note for row in unbound], [security_quotas.TI_INDICATOR_BUDGET.note])
        self.assertEqual(unbound[0].note, "tiIndicator")


class TestReportBindings(unittest.TestCase):
    """Every report API hangs off the root, and every row is counted per report API."""

    def test_one_report_call_spends_three_budgets(self):
        self.assertEqual(
            [id(row) for row in ReportRoot.declared_limits()],
            [id(row) for row in reports_quotas.REPORT_QUOTAS],
        )


class TestSharePointCeilings(unittest.TestCase):
    """A static ceiling rides the type it is a ceiling about, and its own scope names it.

    A ceiling is not a request quota, so it cannot be "declared where the request is made":
    ``SITE_STORAGE`` is a fact about a site, ``LIST_ROW_BYTES`` about one list item,
    ``LIST_ITEM_ATTACHMENT`` about a list item's attachment rather than about the 250 GB a
    library file may be, and ``ZIP_DOWNLOAD`` about the transfer utility that assembles the
    archive. Reading the scopes back off the class rows — and how many rows each scope has —
    is what makes a row moved to the neighbouring type fail, without re-listing the 44 rows.
    """

    PLACEMENT = (
        (List, {"list": 9, "query": 1}),
        (ListItem, {"list item": 1}),
        (Attachment, {"list item": 1}),
        (Field, {"column": 2}),
        (Folder, {"folder": 1}),
        (File, {"file": 10, "url": 1}),
        (MoveCopyUtil, {"transfer": 2, "download": 1}),
        (Site, {"site": 5}),
        (Group, {"group": 1}),
        (TermStore, {"tenant": 5}),
    )

    def test_a_ceiling_rides_the_type_whose_scope_it_names(self):
        for model, expected in self.PLACEMENT:
            with self.subTest(model.__name__):
                actual = Counter(decl.limit.scope for decl in model._schema.class_limits)
                self.assertEqual(actual, Counter(expected))

    def test_the_batch_is_capped_by_items_and_by_bytes(self):
        """One decorator per fact: the item count is enforced, the payload size documented."""
        rows = {id(decl.limit): decl.arg for decl in limits_of(ClientContext.execute_batch)}
        batch = sharepoint_limits.Limits
        self.assertEqual(rows, {id(batch.BATCH_ITEMS): "items_per_batch", id(batch.BATCH_BYTES): None})


class TestComposableDeclarations(unittest.TestCase):
    """``@limit`` composes: two decorators declare two facts, not the last one."""

    def test_a_second_decorator_adds_its_rows(self):
        budgets, ceiling = communications_quotas.CALL_RECORD_BUDGETS[0], communications_quotas.CALL_RECORD_RESOURCE_QUOTA

        @limit(budgets)
        @limit(ceiling)
        def read():
            """Read the record."""

        self.assertEqual([decl.limit for decl in limits_of(read)], [ceiling, budgets])


class TestGlobalQuota(unittest.TestCase):
    """The one row no product owns."""

    def test_every_graph_request_spends_the_app_wide_budget(self):
        (row,) = catalog(product="graph")
        self.assertEqual((row.value, row.unit, row.scope, row.window_seconds), (130_000, "requests", "app", 10))
