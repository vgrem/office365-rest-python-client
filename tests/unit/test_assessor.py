"""Offline tests for the migration assessor — inaccessible lists are skipped, not fatal."""

from __future__ import annotations

import json as jsonlib
import unittest

from office365.migration import MigrationAssessor
from office365.migration.assessment.report import AssessmentReport
from office365.runtime.transport.base import BaseTransport
from office365.sharepoint.client_context import ClientContext
from requests import Response

_DENIED = {
    "error": {
        "code": "-2147024891, System.UnauthorizedAccessException",
        "message": {"value": "Access is denied."},
    }
}


def _list(list_id: str, title: str) -> dict:
    return {"__metadata": {"type": "SP.List"}, "Id": list_id, "Title": title, "Hidden": False}


def _file_item() -> dict:
    return {
        "__metadata": {"type": "SP.ListItem"},
        "FileRef": "/sites/x/Shared Documents/a.txt",
        "FileLeafRef": "a.txt",
        "File": {"__metadata": {"type": "SP.File"}, "Length": 100},
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
        if isinstance(payload, tuple) and payload[0] == "deny":
            resp.status_code = 403
            resp.headers.update({"Content-Type": "application/json"})
            resp._content = jsonlib.dumps(_DENIED).encode("utf-8")
        else:
            resp.status_code = 200
            resp.headers.update({"Content-Type": "application/json;odata=verbose"})
            resp._content = jsonlib.dumps(payload).encode("utf-8")
        return resp


class TestAssessorResilience(unittest.TestCase):
    def _assess(self, transport) -> MigrationAssessor:
        ctx = ClientContext("https://contoso.sharepoint.com/sites/x")
        ctx.pending_request().beforeExecute.clear()
        ctx.pending_request().transport = transport
        return MigrationAssessor(ctx.web)

    def test_inaccessible_list_is_skipped_not_fatal(self):
        transport = _ScriptedTransport(
            [
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

        from office365.migration.assessment.scanners import FieldScanner

        report = AssessmentReport()
        FieldScanner().run(
            [SimpleNamespace(properties=f) for f in fields],
            report,
            location="lists/L",
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
