"""Invitations — creating invitations for external users.

Tests cover:
  - Creating an invitation for an external user
"""

from __future__ import annotations

from tests.decorators import requires_application
from tests.graph_case import GraphApplicationTestCase


class TestInvitations(GraphApplicationTestCase):
    """External user invitation creation."""

    @requires_application("User.Invite.All", "Directory.ReadWrite.All", "User.ReadWrite.All")
    def test_01_create_invitation(self):
        """Creating an invitation for an external user returns a valid resource."""
        invitation = self.client.invitations.create("admin@fabrikam.com", "https://myapp.contoso.com").execute_query()
        self.assertIsNotNone(invitation.resource_path)
        self.assertIsNotNone(invitation.invited_user_email_address)
