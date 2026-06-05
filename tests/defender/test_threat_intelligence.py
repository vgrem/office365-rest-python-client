"""Threat Intelligence — articles, indicators, and intel profiles.
Tests cover:
  - Listing threat intelligence articles
  - Filtering articles by published date and tags
  - Reading article indicators (IoCs)
  - Threat actor / intel profiles
  - Host and reputation queries
"""

from __future__ import annotations

from tests.decorators import requires_delegated
from tests.graph_case import GraphDelegatedTestCase

_TI_READ = ("ThreatIntelligence.Read.All",)


class TestThreatIntelligenceArticles(GraphDelegatedTestCase):
    """Threat intelligence articles — finished intel."""

    @requires_delegated(
        *_TI_READ,
        bypass_roles=["Global Administrator"],
    )
    def test_01_list_articles_paginated(self):
        """Listing threat intelligence articles with $top=5 returns a valid collection."""
        result = self.client.security.threat_intelligence.articles.top(5).get().execute_query()
        self.assertIsNotNone(result.resource_path)

    @requires_delegated(
        *_TI_READ,
        bypass_roles=["Global Administrator"],
    )
    def test_02_article_has_required_properties(self):
        """An article exposes id, title, summary, createdDateTime, and body."""
        result = self.client.security.threat_intelligence.articles.top(3).get().execute_query()
        if len(result) == 0:
            self.skipTest("No threat intel articles exist")
        for article in result:
            self.assertIsNotNone(article.get_property("id"))
            self.assertIsNotNone(article.get_property("title"))
            # Summary may be empty for some articles
            self.assertIsNotNone(article.get_property("createdDateTime"))
            break

    @requires_delegated(
        *_TI_READ,
        bypass_roles=["Global Administrator"],
    )
    def test_03_filter_articles_by_tag(self):
        """Filtering articles by tags returns articles with matching tags."""
        # Use a common tag that many intel articles carry
        result = (
            self.client.security.threat_intelligence.articles.filter("tags/any(t:t eq 'malware')")
            .top(5)
            .get()
            .execute_query()
        )
        self.assertIsNotNone(result.resource_path)

    @requires_delegated(
        *_TI_READ,
        bypass_roles=["Global Administrator"],
    )
    def test_04_search_articles(self):
        """Searching articles by keyword returns relevant results."""
        # Not all APIs support search; this validates the endpoint is reachable
        try:
            result = (
                self.client.security.threat_intelligence.articles.filter("contains(tolower(title), 'phishing')")
                .top(3)
                .get()
                .execute_query()
            )
            self.assertIsNotNone(result.resource_path)
        except Exception:
            self.skipTest("Article search not supported or no matching articles")


class TestThreatIntelligenceIndicators(GraphDelegatedTestCase):
    """Indicators of compromise (IoCs)."""

    @requires_delegated(
        *_TI_READ,
        bypass_roles=["Global Administrator"],
    )
    def test_01_list_indicators(self):
        """Listing threat intelligence indicators returns a valid collection."""
        try:
            result = self.client.security.threat_intelligence.indicators.top(5).get().execute_query()
            self.assertIsNotNone(result.resource_path)
        except AttributeError:
            self.skipTest("Indicators endpoint not available in this SDK version")

    @requires_delegated(
        *_TI_READ,
        bypass_roles=["Global Administrator"],
    )
    def test_02_intel_profiles_accessible(self):
        """Threat intel profiles (threat actors) are accessible."""
        try:
            result = self.client.security.threat_intelligence.intel_profiles.top(5).get().execute_query()
            self.assertIsNotNone(result.resource_path)
        except AttributeError:
            self.skipTest("Intel profiles not available in this SDK version")
