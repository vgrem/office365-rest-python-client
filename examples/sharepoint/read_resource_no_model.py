"""
Demonstrates how to construct and submit requests without a model involved.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/sharepoint-rest-api
"""

import json

from office365.sharepoint.request import SharePointRequest
from tests import test_client_id, test_password, test_site_url, test_tenant, test_username

request = SharePointRequest(test_site_url).with_username_and_password(
    tenant=test_tenant,
    client_id=test_client_id,
    username=test_username,
    password=test_password,
)

try:
    response = request.execute_request("web/currentUser")
    parsed = json.loads(response.content)
    prop_val = parsed["d"]["UserPrincipalName"]
    print("UserPrincipalName: {0}".format(prop_val))
except Exception as e:
    print("An error occurred: {0}".format(e))
