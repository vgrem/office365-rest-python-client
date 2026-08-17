"""
Report sign-ins that used legacy authentication protocols.

Legacy protocols (IMAP, POP, SMTP, Exchange ActiveSync, MAPI, ...) bypass
modern authentication and are a common vector for password-spray attacks.

Requires delegated permission ``AuditLog.Read.All``.

https://learn.microsoft.com/en-us/graph/api/signin-list
"""

import argparse

from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant

LEGACY_PROTOCOLS = ("IMAP", "POP", "SMTP", "Exchange ActiveSync", "MAPI", "Autodiscover")


def main():
    parser = argparse.ArgumentParser(description="Report legacy-auth sign-ins")
    parser.add_argument("--limit", type=int, default=100, help="Number of most-recent sign-ins to scan")
    args = parser.parse_args()

    client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)
    signins = client.audit_logs.signins.top(args.limit).get().execute_query()
    legacy = [s for s in signins if s.client_app_used and any(p in s.client_app_used for p in LEGACY_PROTOCOLS)]

    print(f"Legacy-auth sign-ins ({len(legacy)} of {len(signins)} most recent):\n")
    for s in legacy:
        print(f"  {s.user_principal_name or '?':35s} {s.client_app_used:25s} {s.created_datetime or '?'}")


if __name__ == "__main__":
    main()
