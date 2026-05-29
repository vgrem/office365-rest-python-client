import time
import uuid
from typing import Optional

from office365.outlook.mail.item_body import ItemBody
from office365.teams.channels.channel import Channel
from office365.teams.chats.messages.message import ChatMessage
from office365.teams.team import Team

from tests.decorators import requires_delegated
from tests.graph_case import GraphDelegatedTestCase


class TestGraphChannel(GraphDelegatedTestCase):
    """Tests for channels"""

    target_team: Optional[Team] = None
    target_channel: Optional[Channel] = None
    target_message: Optional[ChatMessage] = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        team_name = "Team_" + uuid.uuid4().hex
        team = cls.client.teams.create(team_name).execute_query()
        cls.target_team = team

    @classmethod
    def tearDownClass(cls):
        if cls.target_team is not None:
            cls.target_team.delete_object().execute_query_retry()

    @requires_delegated(
        "Team.ReadBasic.All", "TeamSettings.Read.All", or_roles=["Global Administrator", "Teams Administrator"]
    )
    def test1_get_team(self):
        """Test getting a team by id"""
        assert TestGraphChannel.target_team is not None
        team = TestGraphChannel.target_team.get().execute_query()
        self.assertIsNotNone(team.id)

    @requires_delegated(
        "Channel.ReadBasic.All",
        "ChannelSettings.Read.All",
        "ChannelSettings.ReadWrite.All",
        "Directory.Read.All",
        "Directory.ReadWrite.All",
        "Group.Read.All",
        "Group.ReadWrite.All",
        or_roles=["Global Administrator", "Teams Administrator"],
    )
    def test2_list_channels(self):
        """Test listing channels for a team"""
        assert TestGraphChannel.target_team is not None
        channels = TestGraphChannel.target_team.channels.get().execute_query()
        self.assertGreater(len(channels), 0)

    @requires_delegated(
        "Channel.Create",
        "Directory.ReadWrite.All",
        "Group.ReadWrite.All",
        or_roles=["Global Administrator", "Teams Administrator"],
    )
    def test3_create_channel(self):
        """Test creating a channel in a team"""
        assert TestGraphChannel.target_team is not None
        channel_name = "Channel_" + uuid.uuid4().hex
        new_channel = TestGraphChannel.target_team.channels.add(display_name=channel_name).execute_query()
        self.assertIsNotNone(new_channel.resource_path)
        TestGraphChannel.target_channel = new_channel

    @requires_delegated(
        "Channel.ReadBasic.All",
        "ChannelSettings.ReadWrite.All",
        "ChannelSettings.Read.All",
        "Directory.Read.All",
        "Directory.ReadWrite.All",
        "Group.Read.All",
        "Group.ReadWrite.All",
        or_roles=["Global Administrator", "Teams Administrator"],
    )
    def test4_get_channel(self):
        """Test getting a specific channel"""
        assert TestGraphChannel.target_channel is not None
        assert TestGraphChannel.target_team is not None
        channel = TestGraphChannel.target_channel
        assert channel.id is not None
        existing_channel = TestGraphChannel.target_team.channels[channel.id].get().execute_query()
        self.assertEqual(existing_channel.id, channel.id)

    @requires_delegated(
        "ChannelMember.Read.All", "ChannelMember.ReadWrite.All", or_roles=["Global Administrator", "Teams Administrator"]
    )
    def test6_list_allowed_members(self):
        """Test listing allowed members of a channel"""
        assert TestGraphChannel.target_channel is not None
        result = TestGraphChannel.target_channel.shared_with_teams.get().execute_query()
        self.assertIsNotNone(result.resource_path)

    @requires_delegated(
        "Channel.ReadBasic.All",
        "ChannelSettings.Read.All",
        "ChannelSettings.ReadWrite.All",
        or_roles=["Global Administrator", "Teams Administrator"],
    )
    def test7_get_primary_channel(self):
        """Test getting the primary channel"""
        assert TestGraphChannel.target_team is not None
        primary_channel = TestGraphChannel.target_team.primary_channel.get().execute_query()
        self.assertIsNotNone(primary_channel.resource_path)

    @requires_delegated("ChannelSettings.ReadWrite.All", or_roles=["Global Administrator", "Teams Administrator"])
    def test9_channel_provision_email(self):
        """Test provisioning email for a channel"""
        assert TestGraphChannel.target_channel is not None
        channel = TestGraphChannel.target_channel
        result = channel.provision_email().execute_query()  # type: ignore[attr-defined]
        self.assertIsNotNone(result.value)  # type: ignore[attr-defined]

    @requires_delegated("ChannelSettings.ReadWrite.All", or_roles=["Global Administrator", "Teams Administrator"])
    def test_10_channel_remove_email(self):
        """Test removing email from a channel"""
        assert TestGraphChannel.target_channel is not None
        channel = TestGraphChannel.target_channel
        result = channel.remove_email().execute_query()  # type: ignore[attr-defined]
        self.assertIsNotNone(result.value)  # type: ignore[attr-defined]

    @requires_delegated(
        "ChannelMessage.Send", "Group.ReadWrite.All", or_roles=["Global Administrator", "Teams Administrator"]
    )
    def test_11_send_message(self):
        """Test sending a message to a channel"""
        assert TestGraphChannel.target_channel is not None
        message = TestGraphChannel.target_channel.messages.add(body=ItemBody("Hello world!")).execute_query()
        self.assertIsNotNone(message.id)
        TestGraphChannel.target_message = message

    @requires_delegated(
        "ChannelMessage.Send", "Group.ReadWrite.All", or_roles=["Global Administrator", "Teams Administrator"]
    )
    def test_12_reply_to_message(self):
        """Test replying to a message"""
        assert TestGraphChannel.target_message is not None
        item_body = ItemBody("Hello world back!")
        reply = TestGraphChannel.target_message.replies.add(body=item_body).execute_query()
        self.assertIsNotNone(reply.id)

    @requires_delegated(
        "Channel.Delete.All",
        "Directory.ReadWrite.All",
        "Group.ReadWrite.All",
        or_roles=["Global Administrator", "Teams Administrator"],
    )
    def test_13_delete_channel(self):
        """Test deleting a channel"""
        assert TestGraphChannel.target_team is not None
        assert TestGraphChannel.target_channel is not None
        channels_before = TestGraphChannel.target_team.channels.get().execute_query()
        TestGraphChannel.target_channel.delete_object().execute_query()
        channels_after = TestGraphChannel.target_team.channels.get().execute_query()
        time.sleep(5)
        self.assertEqual(len(channels_before) - 1, len(channels_after))
