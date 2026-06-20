"""
Generate a new client secret for an application.

After finding an expired secret, use this to create a replacement.
The secretText is only visible at creation time — save it.

Requires delegated permission Application.ReadWrite.All.

https://learn.microsoft.com/en-us/graph/api/application-addpassword
"""

from office365.graph_client import GraphClient
from tests.settings import admin_username, client_id, tenant


def main():
    client = (
        GraphClient(tenant=tenant)
        .with_token_interactive(client_id, admin_username)
        .require_role("Global Administrator", "Privileged Role Administrator")
    )

    app = client.applications.get_by_app_id(client_id)
    result = app.add_password("Rotated secret").execute_query()
    print(f"CLIENT_SECRET={result.value.secretText}")


if __name__ == "__main__":
    main()
