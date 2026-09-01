"""Offline tests for the tenant-scope Large Sites scan (SMAT farm-level report)."""

from __future__ import annotations

import json as jsonlib
import unittest

from office365.migration import MigrationTenantAssessor
from office365.migration.assessment.scanners import AssessmentOptions
from office365.runtime.transport.base import BaseTransport
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.tenant.administration.tenant import Tenant
from requests import Response

_GB = 1024


def _site_props(site_id: str, url: str, storage_mb: int, webs_count: int = 3, owner: str = "owner@contoso.com") -> dict:
    return {
        "__metadata": {"type": "Microsoft.Online.SharePoint.TenantAdministration.SiteProperties"},
        "SiteId": site_id,
        "Url": url,
        "StorageUsageCurrent": storage_mb,
        "WebsCount": webs_count,
        "OwnerLoginName": owner,
        "LastContentModifiedDate": "2024-01-02T03:04:05Z",
        "LockState": "Unlock",
    }


class _ScriptedTransport(BaseTransport):
    def __init__(self, payloads: list) -> None:
        self._payloads = payloads
        self.calls = 0

    def execute(self, request):
        payload = self._payloads[self.calls]
        self.calls += 1
        resp = Response()
        resp.url = request.url
        resp.status_code = 200
        resp.headers.update({"Content-Type": "application/json;odata=verbose"})
        resp._content = jsonlib.dumps(payload).encode("utf-8")
        return resp


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
                        _site_props("1", "https://contoso.sharepoint.com/sites/huge", 700 * _GB, webs_count=12),
                        _site_props("2", "https://contoso.sharepoint.com/sites/small", 50 * _GB, webs_count=2),
                        _site_props("3", "https://contoso.sharepoint.com/sites/exactly", 500 * _GB),
                    ]
                }
            }
        )

        scan = report.scan_reports["LargeSites"]
        self.assertEqual(len(scan.records), 1)
        row = scan.records[0]
        self.assertEqual(row.SiteURL, "https://contoso.sharepoint.com/sites/huge")
        self.assertEqual(row.SizeInGB, 700.0)
        self.assertEqual(row.SiteSizeInMB, 700 * _GB)
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
                        _site_props("1", "https://x/a", 600 * _GB),
                        _site_props("2", "https://x/b", 900 * _GB),
                        _site_props("3", "https://x/c", 700 * _GB),
                    ]
                }
            }
        )
        sizes = [r.SizeInGB for r in report.scan_reports["LargeSites"].records]
        self.assertEqual(sizes, sorted(sizes, reverse=True))

    def test_locked_sites_are_skipped(self):
        locked = _site_props("1", "https://x/locked", 900 * _GB)
        locked["LockState"] = "Locked"
        report = _assess({"d": {"results": [locked, _site_props("2", "https://x/open", 600 * _GB)]}})
        self.assertEqual([r.SiteURL for r in report.scan_reports["LargeSites"].records], ["https://x/open"])

    def test_records_projection_uses_na(self):
        report = _assess({"d": {"results": [_site_props("1", "https://x/a", 600 * _GB)]}})
        scan = report.scan_reports["LargeSites"]
        record = scan.to_records()[0]
        self.assertEqual(record["SiteURL"], "https://x/a")
        self.assertEqual(record["ContentDBName"], "n/a")
        self.assertEqual(record["DistinctUsers"], "n/a")
        self.assertIn("LastContentModifiedDate", scan.to_csv().splitlines()[0])

    def test_site_without_storage_usage_is_skipped(self):
        props = _site_props("1", "https://x/a", 600 * _GB)
        props.pop("StorageUsageCurrent")
        report = _assess({"d": {"results": [props]}})
        self.assertEqual(report.scan_reports, {})

    def test_tenant_access_denied_is_warning_not_fatal(self):
        _denied = {
            "error": {
                "code": "-2147024891, System.UnauthorizedAccessException",
                "message": {"value": "Access is denied."},
            }
        }

        ctx = ClientContext("https://contoso-admin.sharepoint.com")
        ctx.pending_request().beforeExecute.clear()

        class _Deny(_ScriptedTransport):
            def execute(self, request):
                self.calls += 1
                resp = Response()
                resp.url = request.url
                resp.status_code = 403
                resp.headers.update({"Content-Type": "application/json"})
                resp._content = jsonlib.dumps(_denied).encode("utf-8")
                return resp

        ctx.pending_request().transport = _Deny([])
        report = MigrationTenantAssessor(Tenant(ctx)).assess().execute_query().value
        access = [i for i in report.issues if i.category == "access"]
        self.assertEqual(len(access), 1)
        self.assertEqual(report.scan_reports, {})


if __name__ == "__main__":
    unittest.main()
