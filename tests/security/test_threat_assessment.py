from typing import Optional

from tests.decorators import requires_delegated
from tests.graph_case import GraphDelegatedTestCase


class TestThreatAssessment(GraphDelegatedTestCase):
    threat_assessment_request: Optional[object] = None

    @requires_delegated("ThreatAssessment.ReadWrite.All", bypass_roles=["Global Administrator"])
    def test1_create_url_assessment(self):
        """Create a URL threat assessment request."""
        result = self.client.information_protection.create_url_assessment(
            "http://test.com", "block", "phishing"
        ).execute_query()
        self.assertIsNotNone(result.resource_path)
        TestThreatAssessment.threat_assessment_request = result
        assert TestThreatAssessment.threat_assessment_request is not None

    @requires_delegated("ThreatAssessment.ReadWrite.All", bypass_roles=["Global Administrator"])
    def test2_create_file_assessment(self):
        """Create a file threat assessment request."""
        result = self.client.information_protection.create_file_assessment(
            "test.txt", "VGhpcyBpcyBhIHRlc3QgZmlsZQ==", "block", "malware"
        ).execute_query()
        self.assertIsNotNone(result.resource_path)

    @requires_delegated("ThreatAssessment.ReadWrite.All", bypass_roles=["Global Administrator"])
    def test3_create_email_file_assessment(self):
        """Create an email file threat assessment request."""
        result = self.client.information_protection.create_email_file_assessment(
            "tifc@contoso.com", "VGhpcyBpcyBhIHRlc3QgZmlsZQ==", "block", "malware"
        ).execute_query()
        self.assertIsNotNone(result.resource_path)

    @requires_delegated("ThreatAssessment.ReadWrite.All", bypass_roles=["Global Administrator"])
    def test4_list_threat_assessment_requests(self):
        """List threat assessment requests."""
        col = self.client.information_protection.threat_assessment_requests.get().execute_query()
        self.assertIsNotNone(col.resource_path)
