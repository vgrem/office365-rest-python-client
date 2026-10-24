"""A context to hydrate a sidecar into the model with: nothing is queried, so no credentials."""

from __future__ import annotations

import functools

from office365.runtime.client_runtime_context import ClientRuntimeContext


@functools.lru_cache(maxsize=1)
def offline_context() -> ClientRuntimeContext:
    """The one context the records share: a model object cannot exist without one."""
    from office365.graph_client import GraphClient  # local: the client imports every service

    return GraphClient(lambda: {"access_token": "-", "token_type": "Bearer"})
