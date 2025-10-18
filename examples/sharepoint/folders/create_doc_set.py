"""
Create a new Document Set

https://support.microsoft.com/en-us/office/introduction-to-document-sets-3dbcd93e-0bed-46b7-b1ba-b31de2bcd234
"""

from office365.sharepoint.client_context import ClientContext
from tests import test_client_credentials, test_team_site_url

client = ClientContext(test_team_site_url).with_credentials(test_client_credentials)
lib = client.web.default_document_library()
doc_set = lib.create_document_set("10").execute_query()
print(f"DocSet created: {doc_set.name}")
