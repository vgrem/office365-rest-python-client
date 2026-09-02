"""Offline tests for the container-scoped scanner contract."""

from __future__ import annotations

import unittest

from office365.migration.assessment.containers import ScanContainer
from office365.migration.assessment.registry import active_scan_pairs
from office365.migration.assessment.report import AssessmentReport
from office365.migration.assessment.scanners import (
    AssessmentOptions,
    ScanTarget,
    SiteScanSummary,
    SiteStorageScanner,
)

_GB = 1024**3


class TestScanContainerDispatch(unittest.TestCase):
    def test_active_pairs_ignore_disabled_and_respect_containers(self):
        options = AssessmentOptions()  # permissions disabled by default
        active = active_scan_pairs(options)
        names = {definition.name for definition, _ in active}
        self.assertIn("fields", names)
        self.assertIn("paths", names)
        self.assertIn("LargeSites", names)
        self.assertNotIn("permissions", names)

        options.disabled_scans.discard("permissions")
        active = active_scan_pairs(options)
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
            storage_bytes=600 * _GB,
            hits=7,
            web_count=3,
            item_count=4000,
        )
        scanner = SiteStorageScanner()
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

    def test_site_storage_scan_small_site_not_flagged(self):
        report = AssessmentReport()
        summary = SiteScanSummary(storage_bytes=50 * _GB, site_url="https://x/small")
        SiteStorageScanner().run(ScanTarget(ScanContainer.SITE, summary, "https://x/small"), report)
        self.assertFalse(any(i.category == "site" for i in report.issues))


if __name__ == "__main__":
    unittest.main()
