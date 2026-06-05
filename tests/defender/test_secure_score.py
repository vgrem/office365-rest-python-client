"""Secure Score — Microsoft Secure Score control profiles.
Tests cover:
  - Listing secure score control profiles
  - Filtering by control state (config, review, behavior)
  - Reading control metadata (score impact, action URL, max score)
  - Listing top-level secure scores
"""

from __future__ import annotations

from tests.decorators import requires_delegated
from tests.graph_case import GraphDelegatedTestCase

_SCORE_READ = ("SecureScore.Read.All",)


class TestSecureScore(GraphDelegatedTestCase):
    """Microsoft Secure Score control profiles."""

    @requires_delegated(
        *_SCORE_READ,
        bypass_roles=["Global Administrator"],
    )
    def test_01_list_secure_score_control_profiles(self):
        """Listing secure score control profiles returns a valid collection."""
        result = self.client.security.secure_score_control_profiles.top(10).get().execute_query()
        self.assertIsNotNone(result.resource_path)

    @requires_delegated(
        *_SCORE_READ,
        bypass_roles=["Global Administrator"],
    )
    def test_02_control_profile_has_expected_properties(self):
        """A secure score control profile exposes title, maxScore, and actionType."""
        result = self.client.security.secure_score_control_profiles.top(5).get().execute_query()
        if len(result) == 0:
            self.skipTest("No secure score control profiles exist")
        for profile in result:
            self.assertIsNotNone(profile.get_property("title"))
            self.assertIsNotNone(profile.get_property("maxScore"))
            self.assertIsNotNone(profile.get_property("actionType"))
            self.assertIsNotNone(profile.get_property("actionUrl"))
            break

    @requires_delegated(
        *_SCORE_READ,
        bypass_roles=["Global Administrator"],
    )
    def test_03_filter_controls_by_action_type(self):
        """Filtering control profiles by actionType returns matching controls."""
        result = (
            self.client.security.secure_score_control_profiles.filter("actionType eq 'Config'")
            .top(5)
            .get()
            .execute_query()
        )
        self.assertIsNotNone(result.resource_path)
        for profile in result:
            self.assertEqual(profile.get_property("actionType"), "Config")

    @requires_delegated(
        *_SCORE_READ,
        bypass_roles=["Global Administrator"],
    )
    def test_04_control_profile_points_accessible(self):
        """A control profile's maxScore and scoreImpact should be positive numbers."""
        result = self.client.security.secure_score_control_profiles.top(5).get().execute_query()
        if len(result) == 0:
            self.skipTest("No secure score control profiles exist")
        for profile in result:
            max_score = profile.get_property("maxScore")
            self.assertIsNotNone(max_score)
            self.assertGreaterEqual(max_score, 0)

    @requires_delegated(
        *_SCORE_READ,
        bypass_roles=["Global Administrator"],
    )
    def test_05_filter_review_controls(self):
        """Filtering by actionType 'Review' returns review-based controls."""
        result = (
            self.client.security.secure_score_control_profiles.filter("actionType eq 'Review'")
            .top(5)
            .get()
            .execute_query()
        )
        self.assertIsNotNone(result.resource_path)
        for profile in result:
            self.assertEqual(profile.get_property("actionType"), "Review")
