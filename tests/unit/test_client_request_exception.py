"""Offline tests for ClientRequestException.from_response classification."""

from __future__ import annotations

import json
import unittest

from office365.runtime.client_request_exception import (
    ClientRequestException,
    DuplicatedObjectException,
    ObjectNotFoundException,
)
from requests import Response


def _make_error_response(body: dict, headers: dict | None = None) -> Response:
    resp = Response()
    resp.status_code = 400
    resp.url = "https://contoso.sharepoint.com/_api/web/lists"
    resp.headers.update(headers or {})
    resp._content = json.dumps(body).encode("utf-8")
    return resp


class TestFromResponse(unittest.TestCase):
    def test_sharepoint_list_already_exists(self):
        body = {
            "error": {
                "code": "-2130575342, Microsoft.SharePoint.SPException",
                "message": {
                    "lang": "en-US",
                    "value": "A list, survey, discussion board, or document library "
                    "with the specified title already exists in this Web site.",
                },
            }
        }
        exc = ClientRequestException.from_response(_make_error_response(body))
        self.assertIsInstance(exc, DuplicatedObjectException)

    def test_message_fallback_already_exists(self):
        body = {
            "error": {
                "code": "-1, System.Exception",
                "message": "A column with this name already exists.",
            }
        }
        exc = ClientRequestException.from_response(_make_error_response(body))
        self.assertIsInstance(exc, DuplicatedObjectException)

    def test_unrelated_error_stays_generic(self):
        body = {
            "error": {
                "code": "-2147024809, System.ArgumentException",
                "message": "Invalid argument.",
            }
        }
        exc = ClientRequestException.from_response(_make_error_response(body))
        self.assertNotIsInstance(exc, DuplicatedObjectException)
        self.assertIsInstance(exc, ClientRequestException)

    def test_field_not_found_maps_to_object_not_found(self):
        body = {
            "error": {
                "code": "-2147024809, System.ArgumentException",
                "message": {"lang": "en-US", "value": 'Field with name "Status" was not found.'},
            }
        }
        exc = ClientRequestException.from_response(_make_error_response(body))
        self.assertIsInstance(exc, ObjectNotFoundException)

    def test_other_errors_not_duplicated(self):
        body = {
            "error": {
                "code": "-2147024894, System.IO.FileNotFoundException",
                "message": "ResourceNotFound",
            }
        }
        exc = ClientRequestException.from_response(_make_error_response(body))
        self.assertNotIsInstance(exc, DuplicatedObjectException)


class TestDiagnostics(unittest.TestCase):
    def test_graph_inner_error_exposed(self):
        body = {
            "error": {
                "code": "TooManyRequests",
                "message": "Please retry again later.",
                "innerError": {
                    "code": "429",
                    "date": "2025-01-01T00:00:00",
                    "request-id": "94fb3b52-452a-4535-a601-69e0a90e3aa2",
                    "status": "429",
                },
            }
        }
        exc = ClientRequestException.from_response(_make_error_response(body))
        self.assertEqual(exc.request_id, "94fb3b52-452a-4535-a601-69e0a90e3aa2")
        assert exc.inner_error is not None
        self.assertEqual(exc.inner_error["status"], "429")

    def test_sharepoint_headers_exposed(self):
        body = {"error": {"code": "-1, System.Exception", "message": "boom"}}
        exc = ClientRequestException.from_response(
            _make_error_response(
                body,
                headers={
                    "SPRequestGuid": "a1b2c3d4-1234-5678-9abc-def012345678",
                    "SPRequestDuration": "127",
                    "X-SharePointHealthScore": "3",
                },
            )
        )
        self.assertEqual(exc.server_guid, "a1b2c3d4-1234-5678-9abc-def012345678")
        self.assertEqual(exc.duration_ms, 127)  # noqa: PLR2004
        self.assertEqual(exc.health_score, 3)  # noqa: PLR2004

    def test_request_id_prefers_headers(self):
        body = {
            "error": {
                "code": "BadRequest",
                "message": "bad",
                "innerError": {"request-id": "from-body"},
            }
        }
        exc = ClientRequestException.from_response(
            _make_error_response(body, headers={"client-request-id": "from-header"})
        )
        self.assertEqual(exc.request_id, "from-header")

    def test_diagnostics_absent(self):
        exc = ClientRequestException.from_response(_make_error_response({"error": {"message": "boom"}}))
        self.assertIsNone(exc.request_id)
        self.assertIsNone(exc.inner_error)
        self.assertIsNone(exc.server_guid)
        self.assertIsNone(exc.duration_ms)
        self.assertIsNone(exc.health_score)


if __name__ == "__main__":
    unittest.main()
