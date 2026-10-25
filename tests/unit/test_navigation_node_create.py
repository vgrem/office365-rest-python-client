"""The create contract of a navigation node, as the live service spells it.

``NavigationNodeCreationInformation`` describes five fields; the REST create body
accepts two. Probed live on a real site (create, read back, delete, tenant left as
found):

* ``AsLastNode`` and ``PreviousNode`` are rejected — *"The property 'AsLastNode'
  does not exist on type 'SP.NavigationNode'"* — so posting the whole object is a 400.
* ``IsExternal`` is the service's own computation: a node created with an off-site
  URL comes back ``IsExternal: true`` whether or not the body said so.
* ``IsVisible`` is ignored on create and on an update at the node's own entity URL
  (``.../Navigation/QuickLaunch(<id>)`` merged with ``{"IsVisible": false}`` reads
  back ``true``), which is why the flag is declared ``readonly``.

So ``add`` builds the two-field entity it was always building. The test exists
because the information object looks like something that should be posted as a
whole, and posting it is the one thing the service will not take.
"""

import json

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.navigation.nodes.creationinformation import (
    NavigationNodeCreationInformation,
)
from tests._scripted_transport import MethodRoutingTransport

#: The id the scripted create answers with.
_NODE_ID = 7

#: A create needs a form digest, and the digest comes from its own request.
_DIGEST = {"d": {"GetContextWebInformation": {"FormDigestValue": "offline-digest", "FormDigestTimeoutSeconds": 1800}}}


def _create(info):
    posted = []

    def capture(request):
        posted.append(request)
        return {"Id": _NODE_ID, "Title": info.Title, "Url": info.Url}

    transport = MethodRoutingTransport(
        [
            ("POST", "contextInfo", _DIGEST),
            ("POST", "/Navigation/QuickLaunch", capture),
        ]
    )
    ctx = ClientContext("https://contoso.sharepoint.com/sites/x")
    ctx.pending_request().transport = transport
    ctx.authentication_context.authenticate_request = lambda request: None
    node = ctx.web.navigation.quick_launch.add(info)
    ctx.execute_query()
    body = posted[0].data
    return (json.loads(body) if isinstance(body, str) else body), node


def test_a_node_is_created_from_the_two_fields_the_service_accepts():
    info = NavigationNodeCreationInformation(
        Title="Docs", Url="https://www.contoso.com/x", IsExternal=True, AsLastNode=True
    )
    body, node = _create(info)

    assert body == {
        "Title": "Docs",
        "Url": "https://www.contoso.com/x",
        "__metadata": {"type": "SP.NavigationNode"},
    }
    assert node.id == _NODE_ID
