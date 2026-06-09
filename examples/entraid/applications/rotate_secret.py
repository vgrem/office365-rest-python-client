"""
Generate a new client secret for an application.

After finding an expired secret, use this to create a replacement.
The secretText is only visible at creation time — save it.

Requires delegated permission Application.ReadWrite.All.

https://learn.microsoft.com/en-us/graph/api/application-addpassword
"""

from office365.graph_client import GraphClient
from tests import test_client_id, test_client_secret, test_tenant


def main():
    client = GraphClient(tenant=test_tenant).with_client_secret(test_client_id, test_client_secret)

    app = client.applications.get_by_app_id(test_client_id)
    result = app.add_password("Rotated secret").execute_query()

    print(f"New secret for {app.display_name or app.app_id}:")
    print(f"  secretText: {result.value.secretText}")
    print(f"  keyId:      {result.value.keyId}")
    print(f"  expires:    {result.value.end_date_time}")


if __name__ == "__main__":
    main()
