"""Offline tests for the migration assessor — inaccessible lists are skipped, not fatal."""

from __future__ import annotations

import unittest

from office365.migration import MigrationAssessor
from office365.migration.assessment.report import AssessmentReport
from office365.sharepoint.client_context import ClientContext
from tests._scripted_transport import ScriptedTransport as _ScriptedTransport


def _list(list_id: str, title: str) -> dict:
    return {"__metadata": {"type": "SP.List"}, "Id": list_id, "Title": title, "Hidden": False}


def _site() -> dict:
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
                _site(),  # site collection metadata (LargeSites scan)
                {"d": {"results": [_list("1", "Restricted"), _list("2", "Public")]}},  # web.lists
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
                _site(),  # site collection metadata (LargeSites scan)
                {"d": {"results": [_list("1", "A"), _list("2", "B")]}},  # web.lists
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
                _site(),  # site collection metadata (LargeSites scan)
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
        from office365.migration.assessment.scanners import FieldScanner, ScanTarget

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


if __name__ == "__main__":
    unittest.main()


class TestRecursiveAssessment(unittest.TestCase):
    def test_site_collection_scan_aggregates(self):
        def _web(url: str) -> dict:
            return {"__metadata": {"type": "SP.Web"}, "Url": url}

        transport = _ScriptedTransport(
            [
                _site(),  # site collection metadata (LargeSites scan)
                {"d": {"results": [_list("1", "RootList")]}},  # root.lists
                {"d": {"Webs": {"results": [_web("https://x/sites/sub1")]}}},  # get_all_webs
                {"d": {"results": []}},  # RootList.fields
                {"d": {"results": [_file_item()]}},  # RootList.items
                {"d": {"Webs": {"results": []}}},  # sub1.webs (recursion, empty)
                {"d": {"results": [_list("2", "SubList")]}},  # sub1.lists
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
