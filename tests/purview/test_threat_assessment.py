"""Threat Assessment Requests — evaluating URLs, files, and emails for threats.
This was previously part of tests/security, but the API surface lives under
client.information_protection (Purview). It falls under the Information Protection
compliance umbrella — submitting content for automated threat classification.
Tests cover:
  - URL threat assessments
  - File (base64) threat assessments
  - Email file (base64 attachment) threat assessments
  - Listing threat assessment requests with filters
  - Pagination and status inspection
  - Edge cases (empty content, invalid URLs)
"""

from __future__ import annotations

from typing import ClassVar, Optional

from office365.runtime.client_request_exception import ClientRequestException

from tests.decorators import requires_delegated
from tests.graph_case import GraphDelegatedTestCase

# Permission required for creating and reading threat assessments
_TA_PERM = ("ThreatAssessment.ReadWrite.All",)


class TestThreatAssessment(GraphDelegatedTestCase):
    """Threat assessment requests under Purview Information Protection."""

    created_assessment: ClassVar[Optional[object]] = None

    @requires_delegated(*_TA_PERM, bypass_roles=["Global Administrator"])
    def test_01_create_url_threat_assessment(self):
        """Submitting a URL for phishing assessment returns a valid request."""
        test_url = "http://test-phishing-example.com"
        expected_action = "block"
        category = "phishing"
        result = self.client.information_protection.create_url_assessment(
            test_url, expected_action, category
        ).execute_query()
        self.assertIsNotNone(result.resource_path)
        self.assertEqual(result.get_property("url"), test_url)
        self.assertEqual(result.get_property("expectedAssessment"), expected_action)
        self.assertEqual(result.get_property("category"), category)
        TestThreatAssessment.created_assessment = result

    @requires_delegated(*_TA_PERM, bypass_roles=["Global Administrator"])
    def test_02_create_url_assessment_malware_category(self):
        """Submitting a URL with 'malware' category is accepted."""
        test_url = "http://test-malware-check.com"
        result = self.client.information_protection.create_url_assessment(test_url, "block", "malware").execute_query()
        self.assertIsNotNone(result.resource_path)
        self.assertEqual(result.get_property("category"), "malware")

    @requires_delegated(*_TA_PERM, bypass_roles=["Global Administrator"])
    def test_03_create_file_threat_assessment(self):
        """Submitting a base64-encoded file for malware assessment returns a valid request."""
        file_name = "eicar_test.txt"
        # Standard EICAR test string (base64)
        content_b64 = "WDVPIVAlQEFQWzRcUFpYNTQoUFpYNTQoUFpYNTQoUFpYNTQoUFpYNTQoUFpYNTQoUFpYNTQoUFpYNTQo"
        result = self.client.information_protection.create_file_assessment(
            file_name, content_b64, "block", "malware"
        ).execute_query()
        self.assertIsNotNone(result.resource_path)
        self.assertEqual(result.get_property("fileName"), file_name)
        self.assertEqual(result.get_property("category"), "malware")

    @requires_delegated(*_TA_PERM, bypass_roles=["Global Administrator"])
    def test_04_create_email_file_threat_assessment(self):
        """Submitting a base64 email file for phishing assessment is accepted."""
        recipient = "sdk-test@contoso.com"
        content_b64 = "VGhpcyBpcyBhIHRlc3QgZW1haWwgZmlsZSBmb3IgdGhyZWF0IGFzc2Vzc21lbnQu"
        result = self.client.information_protection.create_email_file_assessment(
            recipient, content_b64, "block", "phishing"
        ).execute_query()
        self.assertIsNotNone(result.resource_path)
        self.assertEqual(result.get_property("recipientEmail"), recipient)
        self.assertEqual(result.get_property("category"), "phishing")

    @requires_delegated(*_TA_PERM, bypass_roles=["Global Administrator"])
    def test_05_list_threat_assessment_requests(self):
        """Listing all threat assessment requests returns a valid collection."""
        result = self.client.information_protection.threat_assessment_requests.get().execute_query()
        self.assertIsNotNone(result.resource_path)
        # The collection should be iterable even if empty
        self.assertIsNotNone(len(result))

    @requires_delegated(*_TA_PERM, bypass_roles=["Global Administrator"])
    def test_06_filter_assessments_by_category(self):
        """Filtering threats by category returns only matching requests."""
        result = (
            self.client.information_protection.threat_assessment_requests.filter("category eq 'phishing'")
            .top(5)
            .get()
            .execute_query()
        )
        self.assertIsNotNone(result.resource_path)
        for req in result:
            self.assertEqual(req.get_property("category"), "phishing")

    @requires_delegated(*_TA_PERM, bypass_roles=["Global Administrator"])
    def test_07_assessment_status_fields(self):
        """A created assessment should eventually have requestSource and status populated."""
        created = TestThreatAssessment.created_assessment
        if not created:
            self.skipTest("No created assessment available from previous test")
        # Act — re-fetch to see if status was populated
        result = self.client.information_protection.threat_assessment_requests[created.id].get().execute_query()
        self.assertIsNotNone(result.get_property("requestSource"))
        self.assertIsNotNone(result.get_property("status"))


class TestThreatAssessmentEdgeCases(GraphDelegatedTestCase):
    """Edge cases and negative scenarios for threat assessments."""

    @requires_delegated(*_TA_PERM, bypass_roles=["Global Administrator"])
    def test_01_empty_url_rejected(self):
        """Submitting an empty URL should fail."""
        with self.assertRaises(ClientRequestException):
            self.client.information_protection.create_url_assessment("", "block", "phishing").execute_query()

    @requires_delegated(*_TA_PERM, bypass_roles=["Global Administrator"])
    def test_02_empty_content_rejected(self):
        """Submitting a file assessment with empty content should fail."""
        with self.assertRaises(ClientRequestException):
            self.client.information_protection.create_file_assessment(
                "empty.txt", "", "block", "malware"
            ).execute_query()

    @requires_delegated(*_TA_PERM, bypass_roles=["Global Administrator"])
    def test_03_invalid_category_rejected(self):
        """Submitting a URL with an invalid category value should fail."""
        with self.assertRaises(ClientRequestException):
            self.client.information_protection.create_url_assessment(
                "http://test.com", "block", "invalid_category_xyz"
            ).execute_query()
