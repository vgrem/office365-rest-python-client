"""Service incidents — an issue's incident report, downloaded as a document.

``incident_report`` is one of the two declared operations in ``office365.intune``
that this tenant can actually exercise: it needs ``ServiceHealth.Read.All``,
which the app holds, and an issue id, which the tenant always has.
"""

from __future__ import annotations

from tests.decorators import requires_delegated
from tests.graph_case import GraphDelegatedTestCase


class TestServiceIncidents(GraphDelegatedTestCase):
    """Reading what Microsoft published about an outage."""

    @requires_delegated("ServiceHealth.Read.All")
    def test_01_an_incident_reports_itself_as_a_document(self):
        """A published issue answers with a document, not a JSON payload."""
        issues = self.client.admin.service_announcement.issues.top(1).get().execute_query()
        if not len(issues):
            self.skipTest("The tenant has no service announcement to report on")

        report = issues[0].incident_report().execute_query()

        self.assertIsInstance(report.value, bytes)
        self.assertTrue(report.value.startswith(b"PK"), "a docx archive, not an error page")
