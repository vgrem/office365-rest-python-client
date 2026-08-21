"""
List Azure AD directory audit logs via Microsoft Graph.

https://learn.microsoft.com/en-us/graph/api/directoryaudit-list
"""

import argparse

from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant


def main():
    argparse.ArgumentParser(description="List Azure AD directory audit logs").parse_args()

    client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)
    audits = client.audit_logs.directory_audits.top(10).get().execute_query()
    for a in audits:
        print(f"{a.activity_datetime}: {a.activity_display_name} ({a.category})")


if __name__ == "__main__":
    main()
