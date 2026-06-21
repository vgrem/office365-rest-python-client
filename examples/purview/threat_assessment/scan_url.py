"""
Submit URLs and files for threat assessment (phishing, malware).

Requires application permission ``ThreatAssessment.ReadWrite.All``.

https://learn.microsoft.com/en-us/graph/api/informationprotection-post-threatassessmentrequests
"""

from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant

client = (
    GraphClient(tenant=tenant)
    .with_client_secret(client_id, client_secret)
    .require_application_permission("ThreatAssessment.ReadWrite.All")
)

url_result = client.information_protection.create_url_assessment(
    url="http://test-phishing-example.com",
    expected_assessment="block",
    category="phishing",
).execute_query()
print(f"URL assessment: {url_result.url}  ->  {url_result.status}")

file_result = client.information_protection.create_file_assessment(
    file_name="eicar_test.txt",
    content_data="WDVPIVAlQEFQWzRcUFpYNTQoUFpYNTQoUFpYNTQoUFpYNTQoUFpYNTQoUFpYNTQoUFpYNTQoUFpYNTQo",
    expected_assessment="block",
    category="malware",
).execute_query()
print(f"File assessment: {file_result.file_name}  ->  {file_result.status}")
