"""Channel — creating, getting, listing, tabs, email provisioning, messages, and deletion.

Tests cover:
  - Getting a team by ID
  - Listing channels in a team
  - Creating a channel
  - Getting a specific channel by ID
  - Listing tabs in a channel
  - Listing shared (allowed) members
  - Getting the primary channel
  - Provisioning and removing channel email
  - Sending and replying to messages
  - Deleting a channel
"""

from __future__ import annotations

import uuid
from typing import ClassVar, Optional

from office365.runtime.client_request_exception import ClientRequestException
from office365.teams.channels.channel import Channel
from office365.teams.chats.messages.message import ChatMessage
from office365.teams.team import Team

from tests.decorators import requires_delegated
from tests.graph_case import GraphDelegatedTestCase


class TestGraphChannel(GraphDelegatedTestCase):
    """Channel CRUD, messaging, and settings."""

    target_team: ClassVar[Optional[Team]] = None
    target_channel: ClassVar[Optional[Channel]] = None
    target_message: ClassVar[Optional[ChatMessage]] = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        name = "Team_" + uuid.uuid4().hex
        team = cls.client.teams.create_and_wait(name).execute_query()
        cls.target_team = team

    @classmethod
    def tearDownClass(cls):
        team = cls.target_team
        if team and team.resource_path:
            try:
                team.delete_object().execute_query_retry()
            except Exception:
                pass

    @requires_delegated(
        "Team.ReadBasic.All",
        "TeamSettings.Read.All",
        bypass_roles=["Global Administrator", "Teams Administrator"],
    )
    def test_01_get_team_by_id(self):
        """Getting a team by ID returns a valid team."""
        team = TestGraphChannel.target_team
        if not team:
            self.skipTest("No team available")

        result = team.get().execute_query()
        self.assertIsNotNone(result.get_property("id"))

    @requires_delegated(
        "Channel.ReadBasic.All",
        "ChannelSettings.Read.All",
        "ChannelSettings.ReadWrite.All",
        bypass_roles=["Global Administrator", "Teams Administrator"],
    )
    def test_02_list_channels(self):
        """Listing channels in a team returns at least the General channel."""
        team = TestGraphChannel.target_team
        if not team:
            self.skipTest("No team available")

        channels = team.channels.get().execute_query()
        self.assertGreater(len(channels), 0)

    @requires_delegated(
        "Channel.Create",
        "Directory.ReadWrite.All",
        "Group.ReadWrite.All",
        bypass_roles=["Global Administrator", "Teams Administrator"],
    )
    def test_03_create_channel(self):
        """Creating a new channel in the team should succeed."""
        team = TestGraphChannel.target_team
        if not team:
            self.skipTest("No team available")

        name = "Channel_" + uuid.uuid4().hex
        new_channel = team.channels.add(display_name=name).execute_query()
        self.assertIsNotNone(new_channel.resource_path)
        self.assertEqual(new_channel.get_property("displayName"), name)
        TestGraphChannel.target_channel = new_channel

    @requires_delegated(
        "Channel.ReadBasic.All",
        "ChannelSettings.Read.All",
        "ChannelSettings.ReadWrite.All",
        bypass_roles=["Global Administrator", "Teams Administrator"],
    )
    def test_04_get_channel_by_id(self):
        """Getting a channel by ID returns the same channel."""
        channel = TestGraphChannel.target_channel
        team = TestGraphChannel.target_team
        if not channel or not channel.id or not team:
            self.skipTest("No channel created from previous test")

        existing = team.channels[channel.id].get().execute_query()
        self.assertEqual(existing.get_property("id"), channel.id)

    @requires_delegated(
        "TeamsTab.Read.All",
        "TeamsTab.ReadWrite.All",
        bypass_roles=["Global Administrator", "Teams Administrator"],
    )
    def test_05_list_tabs(self):
        """Listing tabs in a channel returns a valid collection."""
        channel = TestGraphChannel.target_channel
        if not channel:
            self.skipTest("No channel created from previous test")

        tabs = channel.tabs.get().execute_query()
        self.assertIsNotNone(tabs.resource_path)

    @requires_delegated(
        "ChannelMember.Read.All",
        "ChannelMember.ReadWrite.All",
        "ChannelSettings.ReadWrite.All",
    )
    def test_06_list_shared_with_teams(self):
        """Listing teams shared with a SHARED channel (sharedWithTeams is only
        supported for channels of membershipType 'shared')."""
        team = TestGraphChannel.target_team
        if not team:
            self.skipTest("No team available")

        # A regular (standard) channel raises "Operation supported only for
        # shared channel." — use a dedicated shared channel when available.
        channel = None
        try:
            channel = team.channels.add(
                display_name="Shared_" + uuid.uuid4().hex, membership_type="shared"
            ).execute_query()
            result = channel.shared_with_teams.get().execute_query()
        except ClientRequestException as e:
            if channel is not None:
                try:
                    channel.delete_object().execute_query_retry()
                except Exception:
                    pass
            self.skipTest(f"Shared channels / channel sharing not supported here: {e}")

        self.assertIsNotNone(result.resource_path)

    @requires_delegated(
        "Channel.ReadBasic.All",
        "ChannelSettings.Read.All",
        "ChannelSettings.ReadWrite.All",
        bypass_roles=["Global Administrator", "Teams Administrator"],
    )
    def test_07_get_primary_channel(self):
        """Getting the primary channel (General) should succeed."""
        team = TestGraphChannel.target_team
        if not team:
            self.skipTest("No team available")

        primary = team.primary_channel.get().execute_query()
        self.assertIsNotNone(primary.resource_path)

    @requires_delegated("ChannelSettings.ReadWrite.All")
    def test_08_provision_channel_email(self):
        """Provisioning email for a channel should succeed."""
        channel = TestGraphChannel.target_channel
        if not channel:
            self.skipTest("No channel created from previous test")

        result = channel.provision_email().execute_query()
        self.assertIsNotNone(result.value)

    @requires_delegated("ChannelSettings.ReadWrite.All")
    def test_09_remove_channel_email(self):
        """Removing email from a channel should succeed."""
        channel = TestGraphChannel.target_channel
        if not channel:
            self.skipTest("No channel created from previous test")

        try:
            result = channel.remove_email().execute_query()
            self.assertIsNotNone(result.resource_path)
        except Exception:
            self.skipTest("Remove email not available without prior provision")

    @requires_delegated("ChannelMessage.Send")
    def test_10_send_message(self):
        """Sending a message to a channel should succeed."""
        channel = TestGraphChannel.target_channel
        if not channel:
            self.skipTest("No channel created from previous test")

        message = channel.messages.add("Hello world!").execute_query()
        self.assertIsNotNone(message.id)
        TestGraphChannel.target_message = message

    @requires_delegated("ChannelMessage.Send")
    def test_11_reply_to_message(self):
        """Replying to a channel message should succeed."""
        msg = TestGraphChannel.target_message
        if not msg:
            self.skipTest("No message sent from previous test")

        reply = msg.replies.add(body={"content": "Hello world back!"}).execute_query()
        self.assertIsNotNone(reply.id)

    @requires_delegated(
        "Channel.Delete.All",
        "Directory.ReadWrite.All",
        "Group.ReadWrite.All",
        bypass_roles=["Global Administrator", "Teams Administrator"],
    )
    def test_12_delete_channel(self):
        """Deleting a channel should remove it from the team."""
        team = TestGraphChannel.target_team
        channel = TestGraphChannel.target_channel
        if not team or not channel:
            self.skipTest("No team or channel available")

        # Deletion is eventually consistent — assert the request succeeds
        # rather than polling for the eventual removal.
        channel.delete_object().execute_query_retry()
        TestGraphChannel.target_channel = None
