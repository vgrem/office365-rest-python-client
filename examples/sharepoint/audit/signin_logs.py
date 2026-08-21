"""
List Azure AD sign-in logs via Microsoft Graph.

https://learn.microsoft.com/en-us/graph/api/signin-list
"""

import argparse

from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant


def main():
    argparse.ArgumentParser(description="List Azure AD sign-in logs").parse_args()

    client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)
    signins = client.audit_logs.signins.top(10).get().execute_query()
    for s in signins:
        assert s.status is not None
        print(
            f"{s.created_datetime}: {s.user_display_name} "
            f"(errorCode={s.status.errorCode}, "
            f"failureReason='{s.status.failureReason}', "
            f"additionalDetails='{s.status.additionalDetails}')"
        )


if __name__ == "__main__":
    main()
