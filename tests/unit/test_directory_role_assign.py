"""Offline tests for ``DirectoryRoleCollection.assign``.

A directory role nobody has activated exists only as a *template*, so activating one means
reading the templates and posting the id of the matching one. A name with no template cannot be
activated at all - and the failure has to say which name, because the alternative was a bare
``AssertionError`` raised while a response was being handled, which reads as a crash with no
subject.
"""

from __future__ import annotations

import pytest
from office365.graph_client import GraphClient
from office365.runtime.http.request_options import HttpMethod
from tests._scripted_transport import RoutingTransport

TEMPLATES = {
    "value": [
        {"id": "17315797-102d-40b4-93e0-432062caca18", "displayName": "Compliance Administrator"},
        {"id": "e6d1a23a-da11-4be4-9570-befc86d067a7", "displayName": "Compliance Data Administrator"},
    ]
}


def _client():
    transport = RoutingTransport([("directoryRoleTemplates", TEMPLATES), ("directoryRoles", {"id": "r1"})])
    client = GraphClient()
    client.pending_request().beforeExecute.clear()
    client.pending_request().transport = transport
    return client, transport


def test_assign_posts_the_template_id():
    client, transport = _client()

    client.directory_roles.assign("Compliance Administrator").execute_query()

    posted = [request for request in transport.requests if request.method == HttpMethod.Post]
    assert len(posted) == 1
    assert posted[0].data["roleTemplateId"] == "17315797-102d-40b4-93e0-432062caca18"


def test_assign_posts_a_role_not_the_directory_object_it_inherits_from():
    """The payload carries its own type name, and the inherited one is wrong.

    ``DirectoryRole`` extends ``DirectoryObject``, and it inherited the base type name with it,
    so every activation was refused with "Invalid payload '@odata.type':
    'microsoft.graph.directoryObject' is not a subtype of 'microsoft.graph.directoryRole'" -
    a message about the payload, naming nothing the caller passed.
    """
    client, transport = _client()

    client.directory_roles.assign("Compliance Administrator").execute_query()

    posted = [request for request in transport.requests if request.method == HttpMethod.Post]
    assert posted[0].data["@odata.type"] == "#microsoft.graph.DirectoryRole"


def test_assign_names_the_role_it_cannot_find():
    client, _ = _client()

    with pytest.raises(ValueError, match="no role template named 'Records Management'"):
        client.directory_roles.assign("Records Management").execute_query()
