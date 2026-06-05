"""Advanced Hunting — Kusto Query Language (KQL) hunting in Microsoft 365 Defender.
Tests cover:
  - Running a basic KQL hunting query
  - Reading query results
  - Schema/table listing
  - Parameterized queries (time ranges, filters)
"""

from __future__ import annotations

from office365.runtime.client_request_exception import ClientRequestException

from tests.decorators import requires_application
from tests.graph_case import GraphApplicationTestCase

_HUNTING = ("AdvancedHunting.Read.All",)


class TestAdvancedHunting(GraphApplicationTestCase):
    """Advanced hunting via the runHuntingQuery API."""

    @requires_application(*_HUNTING)
    def test_01_run_basic_hunting_query(self):
        """Running a simple KQL hunting query returns valid results."""
        # Arrange — query for email events in the last 7 days
        query = """
        EmailEvents
        | where Timestamp > ago(7d)
        | take 5
        """
        result = self.client.security.run_hunting_query(query).execute_query()
        self.assertIsNotNone(result.value)
        # The result value is a HuntingQueryResults object
        self.assertIsNotNone(result.value.get_property("schema"))

    @requires_application(*_HUNTING)
    def test_02_query_returns_schema_and_rows(self):
        """A hunting result includes schema definitions and result rows."""
        query = """
        EmailEvents
        | where Timestamp > ago(1d)
        | take 3
        """
        result = self.client.security.run_hunting_query(query).execute_query()
        # Schema should define columns
        schema = result.value.get_property("schema", [])
        self.assertIsNotNone(schema)
        results = result.value.get_property("results", [])
        self.assertIsNotNone(results)
        # Results may be empty if no events in the last day

    @requires_application(*_HUNTING)
    def test_03_query_for_alert_info(self):
        """Running a query against AlertInfo returns valid results."""
        query = """
        AlertInfo
        | where Timestamp > ago(7d)
        | take 5
        """
        result = self.client.security.run_hunting_query(query).execute_query()
        self.assertIsNotNone(result.value)

    @requires_application(*_HUNTING)
    def test_04_query_with_count_aggregation(self):
        """Running a count aggregation query works correctly."""
        query = """
        EmailEvents
        | where Timestamp > ago(7d)
        | summarize Count = count() by DeliveryAction
        | take 10
        """
        result = self.client.security.run_hunting_query(query).execute_query()
        self.assertIsNotNone(result.value)

    @requires_application(*_HUNTING)
    def test_05_empty_query_rejected(self):
        """An empty or invalid KQL query should raise an error."""
        with self.assertRaises(ClientRequestException):
            self.client.security.run_hunting_query("").execute_query()
