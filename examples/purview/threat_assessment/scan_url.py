"""
Submit URLs and files for threat assessment (phishing, malware).

Threat assessments check content against Microsoft's threat
intelligence to determine whether a URL or file is malicious.

Requires application permission ``ThreatAssessment.ReadWrite.All``.

https://learn.microsoft.com/en-us/graph/api/informationprotection-post-threatassessmentrequests
"""

import sys

from office365.directory.permissions.guard import has_app_permission
from office365.graph_client import GraphClient
from tests import test_client_id, test_client_secret, test_tenant

client = GraphClient(tenant=test_tenant).with_client_secret(test_client_id, test_client_secret)

if not has_app_permission(client, "ThreatAssessment.ReadWrite.All", test_client_id):
    print("Need ThreatAssessment.ReadWrite.All application permission granted to the app.")
    sys.exit(1)

# 1. Assess a URL for phishing
url_result = client.information_protection.create_url_assessment(
    url="http://test-phishing-example.com",
    expected_assessment="block",
    category="phishing",
).execute_query()
print(f"URL assessment: {url_result.url}  →  {url_result.status}")
print(f"  Expected: {url_result.expected_assessment}  Category: {url_result.category}")

# 2. Assess a file (base64) for malware
file_result = client.information_protection.create_file_assessment(
    file_name="eicar_test.txt",
    content_data="WDVPIVAlQEFQWzRcUFpYNTQoUFpYNTQoUFpYNTQoUFpYNTQoUFpYNTQoUFpYNTQoUFpYNTQoUFpYNTQo",
    expected_assessment="block",
    category="malware",
).execute_query()
print(f"File assessment: {file_result.file_name}  →  {file_result.status}")
