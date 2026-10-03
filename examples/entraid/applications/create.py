"""
Register a new application (app registration).

Creates a new application with a display name and sign-in audience.
The returned app object includes the app/client ID needed for authentication.

By default the demo app is deleted again (clean run). Pass ``--keep`` to register
a persistent app and print a ready ``OFFICE365_CLIENT_ID=...`` line.

https://learn.microsoft.com/en-us/graph/api/application-post-applications

https://learn.microsoft.com/en-us/graph/api/resources/application

Requires delegated permission ``Application.ReadWrite.All``.
"""

import argparse

from office365.graph_client import GraphClient
from tests import create_unique_name
from tests.settings import client_id, password, tenant, username


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--name", help="display name (default: DemoApp + random suffix)")
    parser.add_argument("--keep", action="store_true", help="keep the app instead of deleting it")
    args = parser.parse_args()

    client = GraphClient(tenant=tenant).with_username_and_password(client_id, username, password)

    app = client.applications.add(
        args.name or create_unique_name("DemoApp"),
        signInAudience="AzureADMyOrg",
    ).execute_query()
    print(f"App created: {app.display_name} (appId: {app.app_id})")

    if args.keep:
        print()
        print("Add to .env:")
        print(f"OFFICE365_CLIENT_ID={app.app_id}")
    else:
        app.delete_object(True).execute_query()
        print("App cleaned up.")


if __name__ == "__main__":
    main()
