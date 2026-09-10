"""Merged unit tests (consolidated; see git history for originals)."""

from __future__ import annotations

import unittest
from typing import TYPE_CHECKING, cast

from office365.migration import (
    AssessmentOptions,
    ConflictResolution,
    MailboxAssessor,
    MigrationAssessor,
    MigrationJob,
    MigrationOptions,
    MigrationTenantAssessor,
    OutlookOptions,
)
from office365.migration.adapters.filesystem import JsonFileTarget
from office365.migration.assessment.containers import ScanContainer
from office365.migration.assessment.report import AssessmentReport
from office365.migration.assessment.scanners import ScanTarget
from office365.migration.sharepoint.adapters import SharePointListSource
from office365.migration.sharepoint.registry import sharepoint_scan_pairs
from office365.migration.sharepoint.scanners import LargeSitesScanner, SiteScanSummary
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.tenant.administration.tenant import Tenant
from tests._scripted_transport import ScriptedTransport as _ScriptedTransport


def assessor__list(list_id: str, title: str) -> dict:
    return {"__metadata": {"type": "SP.List"}, "Id": list_id, "Title": title, "Hidden": False}


def assessor__site() -> dict:
    return {
        "__metadata": {"type": "SP.Site"},
        "Id": "00000000-0000-0000-0000-000000000001",
        "Url": "https://contoso.sharepoint.com/sites/x",
        "UsageInfo": {},
        "Owner": {"__metadata": {"type": "SP.User"}, "Title": "Site Owner", "Email": "owner@contoso.com"},
    }


def _file_item() -> dict:
    return {
        "__metadata": {"type": "SP.ListItem"},
        "FileRef": "/sites/x/Shared Documents/a.txt",
        "FileLeafRef": "a.txt",
        "File": {"__metadata": {"type": "SP.File"}, "Length": 100},
    }


class TestAssessorResilience(unittest.TestCase):
    def _assess(self, transport) -> MigrationAssessor:
        ctx = ClientContext("https://contoso.sharepoint.com/sites/x")
        ctx.pending_request().beforeExecute.clear()
        ctx.pending_request().transport = transport
        return MigrationAssessor(ctx.web)

    def test_inaccessible_list_is_skipped_not_fatal(self):
        transport = _ScriptedTransport(
            [
                assessor__site(),  # site collection metadata (LargeSites scan)
                {"d": {"results": [assessor__list("1", "Restricted"), assessor__list("2", "Public")]}},  # web.lists
                {"d": {"results": []}},  # web.webs
                {"d": {"results": []}},  # Restricted.fields
                ("deny",),  # Restricted.items -> 403
                {"d": {"results": []}},  # Public.fields
                {"d": {"results": [_file_item()]}},  # Public.items
            ]
        )
        assessor = self._assess(transport)

        report = assessor.assess().execute_query().value

        self.assertEqual(report.total_lists, 2)
        self.assertEqual(report.total_files, 1)  # only the accessible list was scanned
        access = [i for i in report.issues if i.category == "access"]
        self.assertEqual(len(access), 1)
        self.assertIn("lists/Restricted", access[0].location)

    def test_progress_fires_per_list(self):
        transport = _ScriptedTransport(
            [
                assessor__site(),  # site collection metadata (LargeSites scan)
                {"d": {"results": [assessor__list("1", "A"), assessor__list("2", "B")]}},  # web.lists
                {"d": {"results": []}},  # web.webs
                {"d": {"results": []}},  # A.fields
                {"d": {"results": [_file_item()]}},  # A.items
                {"d": {"results": []}},  # B.fields
                {"d": {"results": [_file_item()]}},  # B.items
            ]
        )
        assessor = self._assess(transport)
        seen = []

        assessor.assess(progress=seen.append).execute_query()

        self.assertEqual([p.done for p in seen], [1, 2])  # noqa: PLR2004
        self.assertEqual(seen[-1].total, 2)  # noqa: PLR2004
        self.assertEqual(seen[-1].stage, "assessing")

    def test_unreachable_site_reports_warning(self):
        transport = _ScriptedTransport(
            [
                assessor__site(),  # site collection metadata (LargeSites scan)
                ("deny",),  # web.lists -> 403
                {"d": {"results": []}},  # web.webs
            ]
        )
        assessor = self._assess(transport)

        report = assessor.assess().execute_query().value

        self.assertTrue(report.lists_skipped)
        self.assertIn("n/a", report.summary())
        access = [i for i in report.issues if i.category == "access"]
        self.assertEqual(len(access), 1)
        self.assertIn("web/lists", access[0].location)


class TestFieldScannerNoise(unittest.TestCase):
    def _run(self, fields) -> AssessmentReport:
        from types import SimpleNamespace

        from office365.migration.assessment.containers import ScanContainer
        from office365.migration.sharepoint.scanners import FieldScanner, ScanTarget

        report = AssessmentReport()
        FieldScanner().run(
            ScanTarget(ScanContainer.FIELDS, [SimpleNamespace(properties=f) for f in fields], "lists/L"),
            report,
        )
        return report

    def test_system_fields_are_not_flagged(self):
        report = self._run(
            [
                {"InternalName": "ID", "SchemaXml": '<Field Type="Counter" ReadOnly="TRUE" SourceID="x"/>'},
                {"InternalName": "Created", "SchemaXml": '<Field ReadOnly="TRUE" SourceID="x"/>'},
            ]
        )
        self.assertEqual(report.issues, [])

    def test_user_field_flags_readonly_warning_and_schema_info(self):
        report = self._run(
            [
                {
                    "InternalName": "MyField",
                    "SchemaXml": '<Field Type="Text" ReadOnly="TRUE" SourceID="x" ColName="x"/>',
                },
            ]
        )
        self.assertTrue(any(i.severity == "warning" and i.location.endswith("/MyField") for i in report.issues))
        self.assertTrue(any(i.severity == "info" and i.location.endswith("/MyField") for i in report.issues))


class TestRecursiveAssessment(unittest.TestCase):
    def test_site_collection_scan_aggregates(self):
        def _web(url: str) -> dict:
            return {"__metadata": {"type": "SP.Web"}, "Url": url}

        transport = _ScriptedTransport(
            [
                assessor__site(),  # site collection metadata (LargeSites scan)
                {"d": {"results": [assessor__list("1", "RootList")]}},  # root.lists
                {"d": {"Webs": {"results": [_web("https://x/sites/sub1")]}}},  # get_all_webs
                {"d": {"results": []}},  # RootList.fields
                {"d": {"results": [_file_item()]}},  # RootList.items
                {"d": {"Webs": {"results": []}}},  # sub1.webs (recursion, empty)
                {"d": {"results": [assessor__list("2", "SubList")]}},  # sub1.lists
                {
                    "d": {
                        "results": [
                            {
                                "__metadata": {"type": "SP.Field"},
                                "InternalName": "MyField",
                                "SchemaXml": '<Field ReadOnly="TRUE" SourceID="x"/>',
                            }
                        ]
                    }
                },  # SubList.fields
                {"d": {"results": [_file_item()]}},  # SubList.items
            ]
        )
        ctx = ClientContext("https://contoso.sharepoint.com/sites/x")
        ctx.pending_request().beforeExecute.clear()
        ctx.pending_request().transport = transport

        report = MigrationAssessor(ctx.web).assess().execute_query().value

        self.assertEqual(report.total_webs, 1)
        self.assertEqual(report.total_lists, 2)  # noqa: PLR2004
        self.assertEqual(report.total_files, 2)  # noqa: PLR2004
        locations = [i.location for i in report.issues]
        self.assertTrue(any(loc.startswith("https://x/sites/sub1/lists/") for loc in locations))


def test_report_to_records():
    from office365.migration.assessment.issue import AssessmentIssue
    from office365.migration.assessment.report import AssessmentReport

    report = AssessmentReport()
    report.issues.append(AssessmentIssue("blocker", "path", "/a.txt", "too long", "shorten"))
    records = report.to_records()
    assert records == [
        {"severity": "blocker", "category": "path", "location": "/a.txt", "message": "too long", "suggestion": "shorten"}
    ]


scancontainers__GB = 1024**3


class TestScanContainerDispatch(unittest.TestCase):
    def test_active_pairs_ignore_disabled_and_respect_containers(self):
        options = AssessmentOptions()  # permissions disabled by default
        active = sharepoint_scan_pairs(options)
        names = {definition.name for definition, _ in active}
        self.assertIn("fields", names)
        self.assertIn("paths", names)
        self.assertIn("LargeSites", names)
        self.assertNotIn("permissions", names)

        options.disabled_scans.discard("permissions")
        active = sharepoint_scan_pairs(options)
        self.assertIn("permissions", {definition.name for definition, _ in active})

        containers = {
            definition.name: definition.container
            for definition, _ in active
            if definition.name in ("fields", "paths", "LargeSites")
        }
        self.assertEqual(containers["fields"], ScanContainer.FIELDS)
        self.assertEqual(containers["paths"], ScanContainer.ITEMS)
        self.assertEqual(containers["LargeSites"], ScanContainer.SITE)

    def test_site_storage_scan_builds_record_and_flags(self):
        report = AssessmentReport()
        report.scan_id = "scan-1"
        summary = SiteScanSummary(
            site_id="s1",
            site_url="https://contoso.sharepoint.com/sites/big",
            owner="owner@contoso.com",
            storage_bytes=600 * scancontainers__GB,
            hits=7,
            web_count=3,
            item_count=4000,
        )
        scanner = LargeSitesScanner()
        scanner.run(ScanTarget(ScanContainer.SITE, summary, summary.site_url or ""), report)

        self.assertEqual(len(scanner.records), 1)
        row = scanner.records[0]
        self.assertEqual(row.SizeInGB, 600.0)
        self.assertEqual(row.NumOfWebs, 3)  # noqa: PLR2004
        self.assertEqual(row.TotalItemCount, 4000)  # noqa: PLR2004
        self.assertEqual(row.ScanID, "scan-1")

        flagged = [i for i in report.issues if i.category == "site" and i.severity == "warning"]
        self.assertEqual(len(flagged), 1)
        self.assertEqual(flagged[0].location, "https://contoso.sharepoint.com/sites/big")


class TestSitePrimitives(unittest.TestCase):
    def test_ensure_folders_dedups_and_sorts(self):
        ctx = ClientContext("https://contoso.sharepoint.com/sites/x")
        folder = ctx.web.root_folder
        calls = []

        class _FakeFolders:
            def ensure_by_path(self, path):
                calls.append(path)
                return "folder"

        folder._properties["Folders"] = _FakeFolders()
        result = folder.ensure_folders(["a/b", "a/b", "a/c", "docs"])
        self.assertEqual(result, folder)
        self.assertEqual(calls, ["a/b", "a/c", "docs"])  # deduped, sorted

    def test_ensure_folders_skips_ancestor_paths(self):
        ctx = ClientContext("https://contoso.sharepoint.com/sites/x")
        folder = ctx.web.root_folder
        calls = []

        class _FakeFolders:
            def ensure_by_path(self, path):
                calls.append(path)
                return "folder"

        folder._properties["Folders"] = _FakeFolders()
        # "a/b" is covered by the nested "a/b/c" — only the deepest is ensured
        folder.ensure_folders(["a/b", "a/b/c", "a/b/d"])
        self.assertEqual(calls, ["a/b/c", "a/b/d"])


largesites__GB = 1024**3

_ISOLATED = AssessmentOptions(disabled_scans={"permissions", "fields", "paths", "files"})


def largesites__site(storage_bytes: int | None = None, hits: int | None = None) -> dict:
    payload = {
        "__metadata": {"type": "SP.Site"},
        "Id": "11111111-1111-1111-1111-111111111111",
        "Url": "https://contoso.sharepoint.com/sites/big",
        "Owner": {"__metadata": {"type": "SP.User"}, "Title": "Site Owner", "Email": "owner@contoso.com"},
    }
    if storage_bytes is not None:
        payload["UsageInfo"] = {"Storage": storage_bytes, "Hits": hits}
    return payload


def largesites__list(list_id: str, title: str, item_count: int, last_modified: str) -> dict:
    return {
        "__metadata": {"type": "SP.List"},
        "Id": list_id,
        "Title": title,
        "Hidden": False,
        "ItemCount": item_count,
        "LastItemModifiedDate": last_modified,
    }


def _users(*logins: str) -> dict:
    return {
        "d": {
            "results": [
                {"__metadata": {"type": "SP.User"}, "LoginName": login, "Title": login.split("|")[-1]}
                for login in logins
            ]
        }
    }


class _Base(unittest.TestCase):
    def _assess(self, payloads: list, options: AssessmentOptions | None = None):
        ctx = ClientContext("https://contoso.sharepoint.com/sites/x")
        ctx.pending_request().beforeExecute.clear()
        ctx.pending_request().transport = _ScriptedTransport(payloads)
        return MigrationAssessor(ctx.web, options or _ISOLATED).assess().execute_query().value


class TestLargeSitesScan(_Base):
    def test_large_site_flagged_with_full_row(self):
        report = self._assess(
            [
                largesites__site(storage_bytes=600 * largesites__GB, hits=1000),  # site -> 600GB
                {
                    "d": {
                        "results": [
                            largesites__list("1", "Docs", 1000, "2024-01-02T03:04:05Z"),
                            largesites__list("2", "Assets", 2000, "2024-05-06T07:08:09Z"),
                        ]
                    }
                },
                {"d": {"Webs": {"results": [{"__metadata": {"type": "SP.Web"}, "Url": "https://x/sub1"}]}}},
                {"d": {"Webs": {"results": []}}},  # sub1.webs (get_all_webs recursion)
                {"d": {"results": []}},  # sub1.lists
            ]
        )

        scan = report.scan_reports["LargeSites"]
        self.assertEqual(len(scan.records), 1)
        row = scan.records[0]

        self.assertEqual(row.SiteId, "11111111-1111-1111-1111-111111111111")
        self.assertEqual(row.SiteURL, "https://contoso.sharepoint.com/sites/big")
        self.assertEqual(row.SiteOwner, "Site Owner")
        self.assertEqual(row.SiteSizeInMB, round(600 * 1024, 1))
        self.assertEqual(row.SizeInGB, 600.0)
        self.assertEqual(row.NumOfWebs, 1)
        self.assertEqual(row.TotalItemCount, 3000)  # noqa: PLR2004
        self.assertEqual(row.Hits, 1000)  # noqa: PLR2004
        self.assertIn("2024-05-06T07:08:09", row.LastContentModifiedDate.isoformat())
        self.assertIsNone(row.ContentDBName)
        self.assertIsNone(row.ContentDBServerName)
        self.assertIsNone(row.ContentDBSizeInMB)
        self.assertIsNone(row.DistinctUsers)
        self.assertIsNone(row.DaysOfUsageData)
        self.assertEqual(row.ScanID, report.scan_id)

        # the exported/neutral form renders unavailable fields as n/a
        record = scan.to_records()[0]
        self.assertEqual(record["ContentDBName"], "n/a")
        self.assertEqual(record["DistinctUsers"], "n/a")

        flagged = [i for i in report.issues if i.category == "site" and i.severity == "warning"]
        self.assertEqual(len(flagged), 1)
        self.assertIn("600.0GB", flagged[0].message)
        self.assertIn("500", flagged[0].message)

    def test_small_site_not_flagged(self):
        report = self._assess(
            [
                largesites__site(storage_bytes=50 * largesites__GB, hits=10),
                {"d": {"results": [largesites__list("1", "Docs", 5, "2024-01-02T03:04:05Z")]}},
                {"d": {"Webs": {"results": []}}},
            ]
        )

        scan = report.scan_reports["LargeSites"]
        self.assertEqual(scan.records[0].SizeInGB, 50.0)
        self.assertFalse(any(i.category == "site" and i.severity == "warning" for i in report.issues))

    def test_usage_info_unavailable_reports_na(self):
        report = self._assess(
            [
                largesites__site(),  # no UsageInfo
                {"d": {"results": [largesites__list("1", "Docs", 5, "2024-01-02T03:04:05Z")]}},
                {"d": {"Webs": {"results": []}}},
            ]
        )

        row = report.scan_reports["LargeSites"].records[0]
        self.assertIsNone(row.SiteSizeInMB)
        self.assertIsNone(row.SizeInGB)
        self.assertIsNone(row.Hits)
        record = report.scan_reports["LargeSites"].to_records()[0]
        self.assertEqual(record["SiteSizeInMB"], "n/a")
        self.assertEqual(record["SizeInGB"], "n/a")
        self.assertEqual(record["Hits"], "n/a")
        self.assertFalse(any(i.category == "site" for i in report.issues))

    def test_disabling_scan_drops_site_query_and_report(self):
        options = AssessmentOptions(disabled_scans={"permissions", "fields", "paths", "files", "LargeSites"})
        ctx = ClientContext("https://contoso.sharepoint.com/sites/x")
        ctx.pending_request().beforeExecute.clear()
        transport = _ScriptedTransport(
            [
                {"d": {"results": [largesites__list("1", "Docs", 5, "2024-01-02T03:04:05Z")]}},  # web.lists
                {"d": {"results": []}},  # web.webs
            ]
        )
        ctx.pending_request().transport = transport
        report = MigrationAssessor(ctx.web, options).assess().execute_query().value

        self.assertEqual(transport.calls, 2)  # noqa: PLR2004 — site query not issued
        self.assertEqual(report.scan_reports, {})

    def test_include_site_admins_queries_owner_group(self):
        report = self._assess(
            [
                largesites__site(storage_bytes=1 * largesites__GB, hits=5),
                {"d": {"results": [largesites__list("1", "Docs", 5, "2024-01-02T03:04:05Z")]}},
                {"d": {"Webs": {"results": []}}},
                _users("i:0#.f|membership|alice@contoso.com", "bob@contoso.com"),
            ],
            options=AssessmentOptions(
                disabled_scans={"permissions", "fields", "paths", "files"},
                include_site_admins=True,
            ),
        )

        row = report.scan_reports["LargeSites"].records[0]
        self.assertIn("alice@contoso.com", row.SiteAdmins)
        self.assertIn("bob@contoso.com", row.SiteAdmins)

    def test_summary_includes_scan_counts(self):
        report = self._assess(
            [
                largesites__site(storage_bytes=1 * largesites__GB, hits=5),
                {"d": {"results": [largesites__list("1", "Docs", 5, "2024-01-02T03:04:05Z")]}},
                {"d": {"Webs": {"results": []}}},
            ]
        )
        self.assertIn("LargeSites: 1", report.summary())


_GB_BYTES = 1024**3  # a gigabyte, in bytes


def _site_props(site_id: str, url: str, storage_gb: int, webs_count: int = 3, owner: str = "owner@contoso.com") -> dict:
    return {
        "__metadata": {"type": "Microsoft.Online.SharePoint.TenantAdministration.SiteProperties"},
        "SiteId": site_id,
        "Url": url,
        "StorageUsage": storage_gb * _GB_BYTES,
        "WebsCount": webs_count,
        "OwnerLoginName": owner,
        "LastContentModifiedDate": "2024-01-02T03:04:05Z",
        "LockState": "Unlock",
    }


def _assess(payload: dict, options: AssessmentOptions | None = None):
    ctx = ClientContext("https://contoso-admin.sharepoint.com")
    ctx.pending_request().beforeExecute.clear()
    ctx.pending_request().transport = _ScriptedTransport([payload])
    return MigrationTenantAssessor(Tenant(ctx), options or AssessmentOptions()).assess().execute_query().value


class TestTenantLargeSites(unittest.TestCase):
    def test_reports_only_sites_over_500gb(self):
        report = _assess(
            {
                "d": {
                    "results": [
                        _site_props("1", "https://contoso.sharepoint.com/sites/huge", 700, webs_count=12),
                        _site_props("2", "https://contoso.sharepoint.com/sites/small", 50, webs_count=2),
                        _site_props("3", "https://contoso.sharepoint.com/sites/exactly", 500),
                    ]
                }
            }
        )

        scan = report.scan_reports["LargeSites"]
        self.assertEqual(len(scan.records), 1)
        row = scan.records[0]
        self.assertEqual(row.SiteURL, "https://contoso.sharepoint.com/sites/huge")
        self.assertEqual(row.SizeInGB, 700.0)
        self.assertEqual(row.SiteSizeInMB, 700 * 1024)  # noqa: PLR2004
        self.assertEqual(row.NumOfWebs, 12)  # noqa: PLR2004
        self.assertEqual(row.SiteOwner, "owner@contoso.com")
        self.assertEqual(row.SiteId, "1")
        self.assertEqual(row.ScanID, report.scan_id)
        self.assertIsNotNone(row.LastContentModifiedDate)

    def test_rows_sorted_largest_first(self):
        report = _assess(
            {
                "d": {
                    "results": [
                        _site_props("1", "https://x/a", 600),
                        _site_props("2", "https://x/b", 900),
                        _site_props("3", "https://x/c", 700),
                    ]
                }
            }
        )
        sizes = [r.SizeInGB for r in report.scan_reports["LargeSites"].records]
        self.assertEqual(sizes, sorted(sizes, reverse=True))

    def test_locked_sites_are_skipped(self):
        locked = _site_props("1", "https://x/locked", 900)
        locked["LockState"] = "Locked"
        report = _assess({"d": {"results": [locked, _site_props("2", "https://x/open", 600)]}})
        self.assertEqual([r.SiteURL for r in report.scan_reports["LargeSites"].records], ["https://x/open"])

    def test_records_projection_uses_na(self):
        report = _assess({"d": {"results": [_site_props("1", "https://x/a", 600)]}})
        scan = report.scan_reports["LargeSites"]
        record = scan.to_records()[0]
        self.assertEqual(record["SiteURL"], "https://x/a")
        self.assertEqual(record["ContentDBName"], "n/a")
        self.assertEqual(record["DistinctUsers"], "n/a")
        self.assertIn("LastContentModifiedDate", scan.to_csv().splitlines()[0])

    def test_site_without_storage_usage_is_skipped(self):
        props = _site_props("1", "https://x/a", 600)
        props.pop("StorageUsage")
        report = _assess({"d": {"results": [props]}})
        self.assertEqual(report.scan_reports, {})

    def test_tenant_access_denied_is_warning_not_fatal(self):
        ctx = ClientContext("https://contoso-admin.sharepoint.com")
        ctx.pending_request().beforeExecute.clear()
        ctx.pending_request().transport = _ScriptedTransport([("deny",)])
        report = MigrationTenantAssessor(Tenant(ctx)).assess().execute_query().value
        access = [i for i in report.issues if i.category == "access"]
        self.assertEqual(len(access), 1)
        self.assertEqual(report.scan_reports, {})


if TYPE_CHECKING:
    from office365.sharepoint.folders.folder import Folder
    from office365.sharepoint.lists.list import List as SPList
    from office365.sharepoint.webs.web import Web


class _Item:
    def __init__(self, item_id: int, properties: dict):
        self.id = item_id
        self.properties = properties


class _Field:
    def __init__(self, internal_name: str, type_as_string: str = "", schema_xml: str = "", hidden: bool = False):
        self.internal_name = internal_name
        self.type_as_string = type_as_string
        self.schema_xml = schema_xml
        self.hidden = hidden


class _Query:
    def __init__(self, load, select):
        self._load = load
        self._select = select

    def execute_query(self):
        return self._load(self._select)


class _ItemsEndpoint:
    def __init__(self, load):
        self._load = load
        self._select = None

    def select(self, columns: list[str]):
        self._select = columns
        return self

    def get_all(self):
        return _Query(self._load, self._select)


class _List:
    def __init__(self, title: str, load, fields: list[_Field]):
        self.title = title
        self.items = _ItemsEndpoint(load)

        class _FieldsEndpoint:
            def get(self):
                return _Query(lambda _: fields, None)

        self.fields = _FieldsEndpoint()


class _TaxonomyError(Exception):
    """Duck-type of a ClientRequestException from an orphaned term set."""

    def __init__(self):
        super().__init__("The given guid does not exist in the term store")
        self.code = "-2146232832, Microsoft.SharePoint.SPFieldValidationException"
        self.message = "The given guid does not exist in the term store"


class _Opaque:
    """A SharePoint-entity-like value with no JSON representation."""

    def __str__(self):
        return "<opaque value>"


def test_export_and_verify_with_opaque_values(tmp_path):
    """Records with entity values still export, checksum, and verify cleanly."""
    loaded = [_Item(1, {"Id": 1, "Title": "hello", "Opaque": _Opaque()})]
    source = SharePointListSource(cast("SPList", _List("Docs", lambda _: loaded, [])))
    job = MigrationJob(source, JsonFileTarget(tmp_path / "out"))

    manifest = job.plan()
    assert len(manifest) == 1
    stats = job.run()
    assert stats.errors == 0

    assert (tmp_path / "out" / "1.json").exists()
    assert job.verify().ok


def test_healthy_list_uses_full_read_without_warnings():
    loaded = [_Item(1, {"Id": 1, "Title": "a"}), _Item(2, {"Id": 2, "Title": "b"})]
    calls = []

    def load(select):
        calls.append(select)
        return loaded

    source = SharePointListSource(cast("SPList", _List("Docs", load, [])))
    result = source.list_items()

    assert len(result) == 2  # noqa: PLR2004
    assert calls == [None]  # full read, no select, no fallback
    assert source.warnings == []
    assert source.read(result[0]) == {"Id": 1, "Title": "a"}


def test_taxonomy_failure_falls_back_to_safe_select():
    selects = []

    def load(select):
        selects.append(select)
        if select is None:
            raise _TaxonomyError()
        return [_Item(1, {k: "" for k in select})]

    fields = [
        _Field("Id"),
        _Field("Title"),
        _Field("Topics", type_as_string="TaxonomyFieldType"),
        _Field("Tags", schema_xml='<Field ... TermSetId="1234-..."/>'),
        _Field("MainLinkSettings", hidden=True),  # restricted system column
    ]
    source = SharePointListSource(cast("SPList", _List("Docs", load, fields)))
    result = source.list_items()

    assert len(result) == 1
    assert any("excluded Managed Metadata" in w for w in source.warnings)
    fallback = selects[-1]
    assert "Topics" not in fallback and "Tags" not in fallback
    assert "MainLinkSettings" not in fallback  # hidden/system columns are not projected
    assert "Title" in fallback
    # records no longer materialize the orphaned taxonomy column
    assert "Topics" not in source.read(result[0])


def test_safe_read_denied_cascades_to_id_title_only():
    selects = []

    def load(select):
        selects.append(select)
        if select is None:
            raise _TaxonomyError()
        if len(select) > 2:  # noqa: PLR2004 — the visible-column read is denied too
            raise PermissionError("denied")
        return [_Item(1, {"Id": 1, "Title": "only"})]

    fields = [_Field("Id"), _Field("Title"), _Field("Notes")]
    source = SharePointListSource(cast("SPList", _List("Docs", load, fields)))
    result = source.list_items()

    assert len(result) == 1
    assert selects[-1] == ["Id", "Title"]
    assert any("denied too" in w for w in source.warnings)


def test_explicit_select_is_honored_and_not_silently_stripped():
    def load(select):
        raise _TaxonomyError()

    source = SharePointListSource(cast("SPList", _List("Docs", load, [])), select=["Id", "Topics"])
    try:
        source.list_items()
    except _TaxonomyError:
        pass
    else:
        raise AssertionError("expected the taxonomy failure to propagate when a select is given")
    assert source.warnings == []


def test_export_rerun_overwrites_and_verifies_clean(tmp_path):
    """Re-running an export into the same folder overwrites and still verifies."""

    loaded = [_Item(1, {"Id": 1, "Title": "hello"})]
    out = tmp_path / "out"

    def make():
        source = SharePointListSource(cast("SPList", _List("Docs", lambda _: loaded, [])))
        return MigrationJob(
            source,
            JsonFileTarget(out),
            options=MigrationOptions(conflict_resolution=ConflictResolution.OVERWRITE),
        )

    job = None
    for _ in range(2):  # noqa: PLR2004
        job = make()
        job.plan()
        stats = job.run()
        assert stats.success == 1 and stats.skipped == 0

    assert job is not None
    assert job.verify().ok


def test_assessor_flags_taxonomy_issue():
    source = type("Web", (), {"context": type("Ctx", (), {})()})()
    assessor = MigrationAssessor(cast("Web", source))
    report = AssessmentReport()

    assessor._flag_access(report, "/sites/x/web/lists/Announcements", _TaxonomyError())
    issue = report.issues[0]
    assert issue.severity == "warning"
    assert issue.category == "taxonomy"
    assert "term" in issue.message
    assert issue.suggestion  # actionable guidance

    # a non-taxonomy failure still gets the generic access warning
    report2 = AssessmentReport()
    assessor._flag_access(report2, "/sites/x/web/lists/Announcements", ValueError("denied"))
    assert report2.issues[0].category == "access"


class _UrlItem:
    def __init__(self, url: str, length: int = 0):
        self.server_relative_url = url
        self.length = length


class _LibraryQuery:
    def __init__(self, result):
        self._result = result

    def execute_query(self):
        return self._result


class _FolderLibrary:
    """A library root whose ServerRelativeUrl is not loaded until requested."""

    def __init__(self, folders, files):
        self.server_relative_url = None
        self._folders = folders
        self._files = files

    def ensure_properties(self, _props):
        self.server_relative_url = "/sites/proj/Shared Documents"
        return _LibraryQuery(self)

    def get_folders(self, recursive=False):
        return _LibraryQuery(self._folders)

    def get_files(self, recursive=False):
        return _LibraryQuery(self._files)


def test_library_source_omits_site_and_library_prefix(tmp_path):
    from office365.migration.sharepoint.adapters import SharePointLibrarySource

    folder = _FolderLibrary(
        folders=[_UrlItem("/sites/proj/Shared Documents/Archive")],
        files=[_UrlItem("/sites/proj/Shared Documents/Forms/Document/1.txt", length=3)],
    )
    source = SharePointLibrarySource(cast("Folder", folder))
    items = source.list_items()

    dests = sorted(i.dest_path for i in items)
    assert dests == ["Archive/", "Forms/Document/1.txt"]  # no site/list prefix
    assert folder.server_relative_url == "/sites/proj/Shared Documents"  # root was loaded


class _FoldersEndpoint:
    """Duck-type of a Graph folder collection (select -> get -> execute)."""

    def __init__(self, items):
        self._items = items
        self._select = None

    def select(self, columns):
        self._select = columns
        return self

    def get(self):
        return self

    def execute_query(self):
        return self._items


class _MailFolder:
    def __init__(self, name, item_count=0, unread_count=0, children=None, folder_id=None):
        self.display_name = name
        self.id = folder_id or name
        self.total_item_count = item_count
        self.unread_item_count = unread_count
        self.child_folder_count = len(children or [])
        self._children = _FoldersEndpoint(children or [])

    @property
    def child_folders(self):
        return self._children


def _root_mailbox(folders):
    class _User:
        mail_folders = _FoldersEndpoint(folders)

    return _User()


def _scan(folders, options=None):
    return MailboxAssessor(_root_mailbox(folders), options or OutlookOptions()).assess()


def test_walker_reports_nested_folders_with_counts():
    inbox = _MailFolder(
        "Inbox",
        item_count=12,
        unread_count=3,
        children=[_MailFolder("Projects", item_count=5, unread_count=1, folder_id="p1")],
    )
    sent = _MailFolder("Sent Items", item_count=4, folder_id="s1")
    report = _scan([inbox, sent])

    scan = report.scan_reports["MailFolders"]
    rows = {row["FolderPath"]: row for row in scan.to_records()}
    assert rows["Inbox"]["ItemCount"] == 12  # noqa: PLR2004
    assert rows["Inbox"]["UnreadItemCount"] == 3  # noqa: PLR2004
    assert rows["Inbox/Projects"]["ItemCount"] == 5  # noqa: PLR2004
    assert rows["Sent Items"]["ItemCount"] == 4  # noqa: PLR2004
    assert report.issues == []


def test_large_folder_is_flagged():
    report = _scan(
        [_MailFolder("Archive", item_count=150_000, folder_id="a1")],
        OutlookOptions(large_folder_items=100_000),
    )
    flags = [i for i in report.issues if i.category == "mail"]
    assert len(flags) == 1
    assert "Archive" in flags[0].location
    assert flags[0].suggestion


def test_disabled_scan_collects_nothing():
    report = _scan([_MailFolder("Inbox", item_count=5, folder_id="i1")], OutlookOptions(disabled_scans={"MailFolders"}))
    assert report.scan_reports == {}
    assert report.issues == []


def test_unreadable_subtree_is_warning_not_fatal():
    broken = _MailFolder("Broken", folder_id="b1")

    class _BrokenEndpoint:
        def select(self, _cols):
            return self

        def get(self):
            return self

        def execute_query(self):
            raise RuntimeError("denied")

    broken._children = _BrokenEndpoint()  # type: ignore[assignment]

    ok = _MailFolder("Inbox", item_count=2, folder_id="i1")
    report = _scan([ok, broken])

    assert report.scan_reports["MailFolders"].records  # healthy folders still reported
    access = [i for i in report.issues if i.category == "access"]
    assert any("Broken" in i.location for i in access)


def test_report_columns_match_record():
    report = _scan([_MailFolder("Inbox", item_count=1, folder_id="i1")])
    header = report.scan_reports["MailFolders"].to_csv().splitlines()[0]
    assert header == "FolderPath,ItemCount,UnreadItemCount,ChildFolderCount"
