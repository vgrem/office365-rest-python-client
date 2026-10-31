"""``ensure_folder`` / ``ensure_file``: create what is missing, reuse what exists.

Both walk the path one segment at a time — a children lookup filtered by name, then a
create when the lookup misses — and address an intermediate folder by its id, never by
path (``/items/{id}:/...`` is the path-addressing form and the server rejects it).
"""

from __future__ import annotations

from office365.graph_client import GraphClient
from tests._scripted_transport import RoutingTransport

_MISS = {"value": []}


def _folder(item_id: str, name: str) -> dict:
    return {"id": item_id, "name": name, "folder": {}, "@odata.type": "#microsoft.graph.driveItem"}


def _file(item_id: str, name: str) -> dict:
    return {"id": item_id, "name": name, "file": {}, "@odata.type": "#microsoft.graph.driveItem"}


def _children(created: dict):
    """A children route: the lookup misses, the create answers the item."""

    def _respond(request):
        return _MISS if request.method.value == "GET" else created

    return _respond


def _client(*routes) -> tuple[GraphClient, RoutingTransport]:
    transport = RoutingTransport(list(routes))
    client = GraphClient()
    client.pending_request().beforeExecute.clear()
    client.pending_request().transport = transport
    return client, transport


def test_ensure_folder_creates_missing_nested_folders():
    client, transport = _client(
        ("drive/root/children", _children(_folder("a1", "a"))),
        ("drive/items/a1/children", _children(_folder("b2", "b"))),
        ("drive/items/b2/children", _children(_folder("c3", "c"))),
    )

    target = client.me.drive.root.ensure_folder("a/b/c")
    client.execute_query()

    assert target.get_property("id") == "c3"
    assert target.get_property("name") == "c"
    # three children lookups + three creates
    assert len(transport.requests) == 6  # noqa: PLR2004
    # the walk descends by id: reads must never use path-addressing on an id
    paths = [url.split("graph.microsoft.com", 1)[-1] for url in transport.calls]
    assert paths[0].startswith("/v1.0/me/drive/root/children")
    assert paths[2].startswith("/v1.0/me/drive/items/a1/children")
    assert paths[4].startswith("/v1.0/me/drive/items/b2/children")
    assert not any(":/" in path for path in paths)


def test_ensure_file_reuses_an_existing_file():
    client, transport = _client(("drive/root/children", {"value": [_file("f1", "f.txt")]}))

    target = client.me.drive.root.ensure_file("f.txt", b"hi")
    client.execute_query()

    (request,) = transport.requests
    assert request.method.value == "GET"
    assert "children" in request.url
    assert "f.txt" in request.url
    assert target.get_property("id") == "f1"


def test_ensure_file_uploads_into_a_missing_folder_chain():
    client, transport = _client(
        (":/f.txt:/content", _file("f4", "f.txt")),
        ("drive/root/children", _children(_folder("a1", "a"))),
        ("drive/items/a1/children", _children(_folder("b2", "b"))),
        # the third level holds no ``f.txt``: the name is what the lookup filters on
        ("drive/items/b2/children", _MISS),
    )

    target = client.me.drive.root.ensure_file("a/b/f.txt", b"hi")
    client.execute_query()

    request = transport.requests[-1]
    assert request.method.value == "PUT"
    assert request.url.endswith("/items/b2:/f.txt:/content")
    assert request.data == b"hi"
    assert target.get_property("id") == "f4"
