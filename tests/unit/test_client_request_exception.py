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


def _make_error_response(body: dict) -> Response:
    resp = Response()
    resp.status_code = 400
    resp.url = "https://contoso.sharepoint.com/_api/web/lists"
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


if __name__ == "__main__":
    unittest.main()
