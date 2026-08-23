"""
Report failed sign-ins across the tenant.

Failed sign-ins are a key security signal — repeated failures can indicate
password-spray or brute-force attacks.

Requires delegated permission ``AuditLog.Read.All``.

https://learn.microsoft.com/en-us/graph/api/signin-list
"""

import argparse

from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant


def main():
    parser = argparse.ArgumentParser(description="Report failed sign-ins")
    parser.add_argument("--top", type=int, default=100, help="number of most-recent sign-ins to scan (default 100)")
    args = parser.parse_args()

    client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)
    signins = client.audit_logs.signins.filter("status/errorCode ne 0").top(args.top).get().execute_query()

    print(f"Failed sign-ins ({len(signins)} of {args.top} most recent):")
    for s in signins:
        reason = s.status.failureReason if s.status else "?"
        error = s.status.errorCode if s.status else "?"
        print(
            f"  {s.created_datetime:%Y-%m-%d %H:%M}  {s.user_principal_name or '?':35s}  "
            f"{s.app_display_name or '?':28s}  code={error}  {reason}"
        )


if __name__ == "__main__":
    main()
