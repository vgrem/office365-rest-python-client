"""``MessageCollection.add_from_mime`` posts a document, not a JSON object (offline).

The MIME import is the one create in the library whose body is the message itself:
Graph parses it, so the request has to be base64 ``text/plain`` and everything else --
recipients, subject, date, attachments -- comes from the headers. The bytes must reach
the wire unchanged, which is what a JSON-serializing create would not do.
"""

from __future__ import annotations

import base64

from office365.graph_client import GraphClient
from office365.runtime.http.request_options import RequestOptions
from tests._scripted_transport import MethodRoutingTransport

_RAW = b'From: Alice <alice@contoso.com>\r\nTo: Bob <bob@contoso.com>\r\nSubject: Q1 "final"\r\n\r\nbody\r\n'


def _client(transport: MethodRoutingTransport) -> GraphClient:
    client = GraphClient()
    client.pending_request().beforeExecute.clear()
    client.pending_request().transport = transport
    return client


def _routes():
    return [
        (
            "POST",
            "/messages",
            {
                "id": "m-1",
                "internetMessageId": "<q1@contoso.com>",
                "subject": 'Q1 "final"',
                "isDraft": True,
            },
        ),
        ("GET", "/mailFolders/inbox", {"id": "inbox", "displayName": "Inbox"}),
    ]


def test_a_mime_document_reaches_the_wire_as_base64_text_unchanged():
    transport = MethodRoutingTransport(_routes())
    folder = _client(transport).me.mail_folders["inbox"].get().execute_query()

    message = (collection := folder.messages).add_from_mime(_RAW)
    collection.context.execute_query()

    posted: RequestOptions = transport.requests[-1]
    assert (posted.method.value, posted.url.endswith("/mailFolders/inbox/messages")) == ("POST", True)
    # ``text/plain`` is the contract; a JSON content type would send a JSON string.
    assert posted.headers.get("Content-Type") == "text/plain"
    assert base64.b64decode(posted.data) == _RAW
    assert message.internet_message_id == "<q1@contoso.com>"
    assert message.is_draft is True
    # The collection holds the object it created, so a caller can address it by id.
    assert list(collection) == [message]
