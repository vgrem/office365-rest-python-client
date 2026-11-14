"""The live client bases: one per auth flow, each holding both service roots.

Two questions are separated here, because conflating them is how a suite ends up signing in
twice or addressing the wrong API:

* **which flow** signs in -- delegated (username/password) or app-only (client secret).
  That is the *base class*: a property of the credentials, not of a test.
* **which root** a test addresses -- ``client`` for v1.0, ``client_beta`` for beta. Both are
  there from ``setUpClass``, so a beta-only family reads ``self.client_beta.device_management
  .intents`` and the test says which root it means by naming it.

Both flows share one MSAL token cache, so the second client of a class is a cache hit rather
than a second sign-in.
"""

from __future__ import annotations

from typing import ClassVar
from unittest import TestCase

import msal
from office365.graph_client import GraphClient
from office365.graph_version import GraphVersion

from tests.settings import settings

#: One cache for the process: MSAL keys entries by client id, authority and scopes, so a
#: delegated and an app-only client cannot answer for one another.
_TOKEN_CACHE = msal.SerializableTokenCache()


class GraphTestCase(TestCase):
    """Common ground: a signed-in client per root, built once per test class."""

    #: The stable client -- what a test means by "the API".
    client: ClassVar[GraphClient] = None  # type: ignore[assignment]

    #: The same credentials against beta: the root that declares the preview-only families.
    client_beta: ClassVar[GraphClient] = None  # type: ignore[assignment]

    @classmethod
    def setUpClass(cls):
        cls.client = cls.sign_in(GraphVersion.V1)
        cls.client_beta = cls.sign_in(GraphVersion.BETA)

    @classmethod
    def sign_in(cls, version: GraphVersion) -> GraphClient:
        """Build and authenticate a client for ``version``. The flow decides how."""
        raise NotImplementedError


class GraphDelegatedTestCase(GraphTestCase):
    """A signed-in user's client (ROPC)."""

    @classmethod
    def sign_in(cls, version: GraphVersion) -> GraphClient:
        settings.require("delegated-ropc")
        return GraphClient(tenant=settings.tenant, version=version, token_cache=_TOKEN_CACHE).with_username_and_password(
            settings.client_id, settings.username, settings.password
        )


class GraphApplicationTestCase(GraphTestCase):
    """An app-only client (client secret)."""

    @classmethod
    def sign_in(cls, version: GraphVersion) -> GraphClient:
        settings.require("app-only")
        return GraphClient(tenant=settings.tenant, version=version, token_cache=_TOKEN_CACHE).with_client_secret(
            settings.client_id, settings.client_secret
        )
