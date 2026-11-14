"""What a failure says: the message a caller reads, and the type the runtime dispatches to.

Nothing is sent here. A payload is handed to the parser the way the runtime hands it over,
and the file's claims are about the text that comes back and the class it comes back as.
"""

from __future__ import annotations

import json

from office365.runtime.client_request_exception import (
    ClientRequestException,
    ErrorPayload,
    _clean_message,
)
from office365.runtime.exceptions import FileLockedException
from requests import Response

#: The Intune proxy wraps ``error.message`` in a JSON object.
INTUNE_MESSAGE = json.dumps({"_version": 3, "Message": "Application is not authorized to perform this operation."})

#: Some services append support diagnostics to an otherwise plain message.
SUPPORT_TAIL = " - Operation ID (for customer support): 00000000-0000-0000-0000-000000000000"

#: A shared lock, as SharePoint spells it: the HRESULT first, then the .NET type.
LOCKED_BODY = (
    b'{"error":{"code":"-2147018894, Microsoft.SharePoint.SPFileLockException",'
    b'"message":"The file report.xlsx is locked for shared use by John Doe [membership]."}}'
)


def _response(body: bytes = LOCKED_BODY, status: int = 423) -> Response:
    response = Response()
    response.status_code = status
    response.url = "https://contoso.sharepoint.com/_api/web"
    response._content = body
    return response


def test_the_intune_proxy_message_is_unwrapped_to_its_inner_text():
    assert _clean_message(INTUNE_MESSAGE) == "Application is not authorized to perform this operation."


def test_a_support_tail_is_dropped_from_a_plain_message():
    assert _clean_message("Access denied." + SUPPORT_TAIL) == "Access denied."


def test_a_plain_message_is_returned_unchanged():
    assert _clean_message("Access denied.") == "Access denied."


def test_a_sharepoint_code_splits_into_an_hresult_and_a_type_name():
    payload = ErrorPayload(code="-2147018894, Microsoft.SharePoint.SPFileLockException")

    assert payload.hresult == "-2147018894"
    assert payload.error_type == "Microsoft.SharePoint.SPFileLockException"


def test_a_symbolic_graph_code_has_neither_hresult_nor_type_name():
    payload = ErrorPayload(code="Authorization_RequestDenied")

    assert payload.hresult is None
    assert payload.error_type is None


def test_a_locked_file_arrives_as_the_lock_exception_and_names_its_owner():
    failed = ClientRequestException.from_response(_response())

    assert isinstance(failed, FileLockedException)
    assert "John Doe" in str(failed)
    assert "shared lock" in str(failed)


def test_a_hint_is_rendered_below_the_message_and_a_blank_one_is_ignored():
    failed = ClientRequestException("Access denied.").add_hint("").add_hint("Requires Sites.Read.All.")

    assert failed.hints == ("Requires Sites.Read.All.",)
    assert str(failed).splitlines() == ["Access denied.", "Requires Sites.Read.All."]
