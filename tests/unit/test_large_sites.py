"""Offline tests for the SMAT-style Large Sites scan."""

from __future__ import annotations

import unittest

from office365.migration import MigrationAssessor
from office365.migration.assessment.scanners import AssessmentOptions
from office365.sharepoint.client_context import ClientContext
from tests._scripted_transport import ScriptedTransport as _ScriptedTransport

_GB = 1024**3

_ISOLATED = AssessmentOptions(disabled_scans={"permissions", "fields", "paths", "files"})


def _site(storage_bytes: int | None = None, hits: int | None = None) -> dict:
    payload = {
        "__metadata": {"type": "SP.Site"},
        "Id": "11111111-1111-1111-1111-111111111111",
        "Url": "https://contoso.sharepoint.com/sites/big",
        "Owner": {"__metadata": {"type": "SP.User"}, "Title": "Site Owner", "Email": "owner@contoso.com"},
    }
    if storage_bytes is not None:
        payload["UsageInfo"] = {"Storage": storage_bytes, "Hits": hits}
    return payload


def _list(list_id: str, title: str, item_count: int, last_modified: str) -> dict:
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
                _site(storage_bytes=600 * _GB, hits=1000),  # site -> 600GB
                {
                    "d": {
                        "results": [
                            _list("1", "Docs", 1000, "2024-01-02T03:04:05Z"),
                            _list("2", "Assets", 2000, "2024-05-06T07:08:09Z"),
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
                _site(storage_bytes=50 * _GB, hits=10),
                {"d": {"results": [_list("1", "Docs", 5, "2024-01-02T03:04:05Z")]}},
                {"d": {"Webs": {"results": []}}},
            ]
        )

        scan = report.scan_reports["LargeSites"]
        self.assertEqual(scan.records[0].SizeInGB, 50.0)
        self.assertFalse(any(i.category == "site" and i.severity == "warning" for i in report.issues))

    def test_usage_info_unavailable_reports_na(self):
        report = self._assess(
            [
                _site(),  # no UsageInfo
                {"d": {"results": [_list("1", "Docs", 5, "2024-01-02T03:04:05Z")]}},
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
                {"d": {"results": [_list("1", "Docs", 5, "2024-01-02T03:04:05Z")]}},  # web.lists
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
                _site(storage_bytes=1 * _GB, hits=5),
                {"d": {"results": [_list("1", "Docs", 5, "2024-01-02T03:04:05Z")]}},
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
                _site(storage_bytes=1 * _GB, hits=5),
                {"d": {"results": [_list("1", "Docs", 5, "2024-01-02T03:04:05Z")]}},
                {"d": {"Webs": {"results": []}}},
            ]
        )
        self.assertIn("LargeSites: 1", report.summary())


if __name__ == "__main__":
    unittest.main()
