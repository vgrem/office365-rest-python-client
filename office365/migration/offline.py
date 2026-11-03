"""A context to hydrate a sidecar into the model with: nothing is queried, so no credentials."""

from __future__ import annotations

import functools

from office365.runtime.client_runtime_context import ClientRuntimeContext


@functools.lru_cache(maxsize=1)
def offline_context() -> ClientRuntimeContext:
    """The one Graph context the records share: a model object cannot exist without one."""
    from office365.graph_client import GraphClient  # local: the client imports every service

    return GraphClient(lambda: {"access_token": "-", "token_type": "Bearer"})


def offline_sharepoint_context() -> ClientRuntimeContext:
    """A SharePoint context at a placeholder address.

    Fresh per call: a caller that queues or retries is the only one holding it, so no
    request state is shared between two models built for two tests.
    """
    from office365.sharepoint.client_context import ClientContext  # local: same reason

    return ClientContext("https://contoso.sharepoint.com")
