"""Offline tests for the ``applications.ensure`` / ``service_principals.ensure`` setup helpers.

Covers the reuse-or-create semantics of ``ApplicationCollection.ensure`` (and its
``create_service_principal`` follow-up), the get-or-create behaviour of
``ServicePrincipalCollection.ensure``, and the Entra ``Request_ResourceNotFound``
classification the latter relies on.
"""

from __future__ import annotations

from office365.graph_client import GraphClient
from office365.runtime.client_request_exception import ClientRequestException
from office365.runtime.exceptions import ObjectNotFoundException
from office365.runtime.http.http_method import HttpMethod
from requests import Response
from tests._scripted_transport import ScriptedTransport

APP_ID = "11111111-1111-1111-1111-111111111111"
APP_OBJECT_ID = "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"
SP_OBJECT_ID = "22222222-2222-2222-2222-222222222222"

_NOT_FOUND = {
    "http_status": 404,
    "body": {
        "error": {
            "code": "Request_ResourceNotFound",
            "message": "Resource does not exist.",
        }
    },
}


class _RecordingTransport(ScriptedTransport):
    """Scripted transport that also records the requests it received."""

    def __init__(self, payloads):
        super().__init__(payloads)
        self.requests = []

    def execute(self, request):
        self.requests.append(request)
        return super().execute(request)


def _client(transport) -> GraphClient:
    client = GraphClient()
    client.pending_request().beforeExecute.clear()
    client.pending_request().transport = transport
    return client


def _methods(transport: _RecordingTransport) -> list[str]:
    return [request.method for request in transport.requests]


def test_ensure_creates_app_when_no_app_id():
    transport = _RecordingTransport([{"id": APP_OBJECT_ID, "appId": APP_ID, "displayName": "my-app"}])
    client = _client(transport)

    app = client.applications.ensure("my-app").execute_query()

    assert app.app_id == APP_ID
    assert _methods(transport) == [HttpMethod.Post]
    assert transport.requests[0].url.endswith("/applications")
    assert transport.requests[0].data["displayName"] == "my-app"


def test_ensure_reuses_app_by_app_id():
    transport = _RecordingTransport([{"id": APP_OBJECT_ID, "appId": APP_ID, "displayName": "my-app"}])
    client = _client(transport)

    app = client.applications.ensure("my-app", APP_ID).execute_query()

    assert app.app_id == APP_ID
    assert _methods(transport) == [HttpMethod.Get]
    assert f"applications(appId='{APP_ID}')" in transport.requests[0].url


def test_ensure_creates_service_principal_for_new_app():
    transport = _RecordingTransport(
        [
            {"id": APP_OBJECT_ID, "appId": APP_ID, "displayName": "my-app"},  # POST applications
            _NOT_FOUND,  # GET servicePrincipals(appId=...) -> missing
            {"id": SP_OBJECT_ID, "appId": APP_ID},  # POST servicePrincipals
        ]
    )
    client = _client(transport)

    app = client.applications.ensure("my-app", create_service_principal=True).execute_query()

    assert app.app_id == APP_ID
    assert _methods(transport) == [HttpMethod.Post, HttpMethod.Get, HttpMethod.Post]
    assert transport.requests[-1].url.endswith("/servicePrincipals")
    assert transport.requests[-1].data["appId"] == APP_ID


def test_ensure_skips_service_principal_when_it_exists():
    transport = _RecordingTransport(
        [
            {"id": APP_OBJECT_ID, "appId": APP_ID, "displayName": "my-app"},  # GET applications
            {"id": SP_OBJECT_ID, "appId": APP_ID},  # GET servicePrincipals -> found
        ]
    )
    client = _client(transport)

    app = client.applications.ensure("my-app", APP_ID, create_service_principal=True).execute_query()

    assert app.app_id == APP_ID
    assert _methods(transport) == [HttpMethod.Get, HttpMethod.Get]


def test_service_principal_ensure_creates_when_missing():
    transport = _RecordingTransport([_NOT_FOUND, {"id": SP_OBJECT_ID, "appId": APP_ID}])
    client = _client(transport)

    sp = client.service_principals.ensure(APP_ID).execute_query()

    assert sp.id == SP_OBJECT_ID
    assert _methods(transport) == [HttpMethod.Get, HttpMethod.Post]
    assert transport.requests[-1].data["appId"] == APP_ID


def test_service_principal_ensure_reuses_existing():
    transport = _RecordingTransport([{"id": SP_OBJECT_ID, "appId": APP_ID}])
    client = _client(transport)

    sp = client.service_principals.ensure(APP_ID).execute_query()

    assert sp.id == SP_OBJECT_ID
    assert _methods(transport) == [HttpMethod.Get]


def test_entra_resource_not_found_is_classified():
    response = Response()
    response.status_code = 404
    response.url = f"https://graph.microsoft.com/v1.0/servicePrincipals(appId='{APP_ID}')"
    response._content = b'{"error":{"code":"Request_ResourceNotFound","message":"Resource does not exist."}}'

    exc = ClientRequestException.from_response(response)

    assert isinstance(exc, ObjectNotFoundException)
