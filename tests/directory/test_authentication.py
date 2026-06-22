"""Authentication — methods, strength policies, and password methods for the current user.

Tests cover:
  - Listing authentication methods for the current user
  - Listing authentication strength policies
  - Listing password methods for the current user
"""

from __future__ import annotations

from tests.decorators import requires_delegated
from tests.graph_case import GraphDelegatedTestCase


class TestAuthentication(GraphDelegatedTestCase):
    """Current user authentication methods and strength policies."""

    @requires_delegated(
        "UserAuthenticationMethod.Read.All",
        "UserAuthenticationMethod.ReadWrite.All",
        bypass_roles=[
            "Authentication Administrator",
            "Privileged Authentication Administrator",
            "Global Administrator",
            "Global Reader",
        ],
    )
    def test_01_list_methods(self):
        """Listing authentication methods for the current user returns a valid collection."""
        result = self.client.me.authentication.methods.get().execute_query()
        self.assertIsNotNone(result.resource_path)

    @requires_delegated(
        "Policy.Read.All",
        "Policy.ReadWrite.ConditionalAccess",
    )
    def test_02_list_strength_policies(self):
        """Listing authentication strength policies returns a valid collection."""
        result = self.client.policies.authentication_strength_policies.get().execute_query()
        self.assertIsNotNone(result.resource_path)

    @requires_delegated(
        "UserAuthenticationMethod.Read",
        "UserAuthenticationMethod.Read.All",
        "UserAuthenticationMethod.ReadWrite",
        "UserAuthenticationMethod.ReadWrite.All",
        bypass_roles=[
            "Authentication Administrator",
            "Privileged Authentication Administrator",
            "Global Administrator",
            "Global Reader",
        ],
    )
    def test_03_list_password_methods(self):
        """Listing password methods for the current user returns a valid collection."""
        result = self.client.me.authentication.password_methods.get().execute_query()
        self.assertIsNotNone(result.resource_path)
