"""A client addresses one API version, and says which.

The version picks the service root only: the model is one tree, so nothing here
asserts that a member is *available* -- that is a fact about the declaration, and
it is only knowable once the beta metadata is in the model too.
"""

from office365.graph_client import GraphClient
from office365.graph_version import GraphVersion

TENANT = "contoso.onmicrosoft.com"
GRAPH = "https://graph.microsoft.com"


def test_the_default_client_addresses_v1():
    client = GraphClient(tenant=TENANT)

    assert client.version is GraphVersion.V1
    assert client.version.value == "v1.0"
    assert client.service_root_url == f"{GRAPH}/v1.0"


def test_a_beta_client_addresses_beta():
    client = GraphClient(tenant=TENANT, version=GraphVersion.BETA)

    assert client.version is GraphVersion.BETA
    assert client.version.value == "beta"
    assert client.service_root_url == f"{GRAPH}/beta"
    assert client.pending_request().service_root_url == f"{GRAPH}/beta"


def test_switching_reaches_a_request_that_already_exists():
    client = GraphClient(tenant=TENANT)
    request = client.pending_request()

    client.version = GraphVersion.BETA

    assert request.version is GraphVersion.BETA
    assert request.service_root_url == f"{GRAPH}/beta"
    assert client.version is GraphVersion.BETA


def test_the_request_is_the_one_place_the_version_lives():
    """Setting it on the request -- the only way to do this before the client had
    a ``version`` -- must not leave a second copy saying something else."""
    client = GraphClient(tenant=TENANT)

    client.pending_request().version = GraphVersion.BETA

    assert client.version is GraphVersion.BETA
    assert client.service_root_url == f"{GRAPH}/beta"


def test_a_version_set_before_the_first_request_seeds_it():
    """With no request yet there is nothing to delegate to, so the seed is what the
    request gets built with once something asks for one."""
    client = GraphClient(tenant=TENANT)

    client.version = GraphVersion.BETA

    assert client.version is GraphVersion.BETA
    assert client.pending_request().service_root_url == f"{GRAPH}/beta"
