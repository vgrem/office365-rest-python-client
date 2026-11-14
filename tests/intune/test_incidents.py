"""Service incidents: an issue's incident report, downloaded as a document.

``incidentReport`` is a *conditional* operation: the service publishes the report for an issue
whose post-incident review has been released, and answers ``404 ObjectNotFoundException`` for
any other issue. Taking ``issues[0]`` therefore fails on a quiet tenant - measured, 60 issues
and none of them reviewed - so the test selects on the property Microsoft documents, and skips
naming what the tenant does not have.

The call needs ``ServiceHealth.Read.All``, which the app holds.
"""

from __future__ import annotations

from tests.decorators import requires_delegated
from tests.intune.intune_case import IntuneCase


class TestServiceIncidents(IntuneCase):
    """Reading what Microsoft published about an outage."""

    @requires_delegated("ServiceHealth.Read.All")
    def test_01_a_reviewed_issue_reports_itself_as_a_document(self):
        """A published review answers with a docx archive, not with JSON."""
        issues = self.client.admin.service_announcement.issues.top(60).get().execute_query()
        self.assertIsNotNone(issues.resource_path)

        reviews = [issue for issue in issues if issue.get_property("postIncidentReviewPublished")]
        if not reviews:
            self.skipTest("no issue on this tenant carries a post-incident review")

        report = reviews[0].incident_report().execute_query()

        self.assertIsInstance(report.value, bytes)
        self.assertTrue(report.value.startswith(b"PK"), "a docx archive, not an error page")

    @requires_delegated("ServiceHealth.Read.All")
    def test_02_an_issue_names_the_service_it_affects(self):
        """The issue table itself is readable, and an issue is classified by service."""
        issues = self.client.admin.service_announcement.issues.top(10).get().execute_query()
        issue = self.row_or_skip(issues, "service announcement")

        self.assertIsInstance(issue.get_property("id"), str)
        self.assertIsNotNone(issue.get_property("service"), "an issue names the service it affects")
