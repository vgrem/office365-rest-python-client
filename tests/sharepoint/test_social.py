"""Tests for SharePoint social features including following, feeds, and suggestions."""

from __future__ import annotations

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.social.following.rest_manager import (
    SocialRestFollowingManager,
)
from office365.sharepoint.social.switch import SPSocialSwitch

from tests import (
    test_client_id,
    test_password,
    test_team_site_url,
    test_tenant,
    test_username,
)
from tests.sharepoint.sharepoint_case import SPTestCase


class TestSocial(SPTestCase):
    """Test SharePoint social features."""

    @classmethod
    def setUpClass(cls):
        super(TestSocial, cls).setUpClass()
        cls.my_client = ClientContext(test_team_site_url).with_username_and_password(
            test_tenant, test_client_id, test_username, test_password
        )

    def test_01_is_following_feature_enabled(self):
        """Check if the following feature is enabled."""
        result = SPSocialSwitch.is_following_feature_enabled(self.my_client).execute_query()
        self.assertIsNotNone(result.value)

    def test_02_create_post(self):
        """Placeholder for creating a social post."""
        # post_data = SocialPostCreationData(content_text="Look at this!")
        # manager = SocialFeedManager(self.my_client)
        # result = manager.create_post(None, post_data).execute_query()
        # self.assertIsNotNone(result.value)

    def test_03_delete_post(self):
        """Placeholder for deleting a social post."""

    def test_04_get_followers(self):
        """Get followers via SocialRestFollowingManager."""
        manager = SocialRestFollowingManager(self.my_client)
        result = manager.my.followers().execute_query()
        self.assertIsNotNone(result.value)

    def test_05_get_followers_alt(self):
        """Get followers via social following manager."""
        result = self.my_client.social_following_manager.get_followers().execute_query()
        self.assertIsNotNone(result.value)

    def test_06_get_suggestions(self):
        """Get suggestions from the social following manager."""
        result = self.my_client.social_following_manager.get_suggestions().execute_query()
        self.assertIsNotNone(result.value)

    # def test8_get_social_feed(self):
    #    feed = SocialRestFeed(self.my_client).get().execute_query()
    #    self.assertIsNotNone(feed.social_feed)

    # def test9_get_feed(self):
    #    result = self.my_client.social_feed_manager.get_feed().execute_query()
    #    self.assertIsNotNone(result.value)
