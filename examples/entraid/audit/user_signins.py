"""
Show the sign-in history for a specific user.

Requires delegated permission ``AuditLog.Read.All``.

https://learn.microsoft.com/en-us/graph/api/signin-list
"""

import argparse

from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant


def main():
    parser = argparse.ArgumentParser(description="Show sign-in history for a user")
    parser.add_argument("--user", required=True, help="User principal name, e.g. user@contoso.com")
    parser.add_argument("--limit", type=int, default=20, help="Max sign-ins to show")
    args = parser.parse_args()

    client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)
    signins = (
        client.audit_logs.signins.filter(f"userPrincipalName eq '{args.user}'")
        .top(args.limit)
        .get()
        .execute_query()
    )

    print(f"Sign-ins for {args.user} ({len(signins)}):\n")
    for s in signins:
        code = s.status.errorCode if s.status else None
        print(f"  {s.created_datetime or '?':30s} {s.client_app_used or '?':20s} {s.app_display_name or '?'}"
              f"  (code {code})")


if __name__ == "__main__":
    main()
