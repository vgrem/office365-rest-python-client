"""
Report which apps / service principals are being signed into.

Requires delegated permission ``AuditLog.Read.All``.

https://learn.microsoft.com/en-us/graph/api/signin-list
"""

import argparse
from collections import Counter

from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant


def main():
    parser = argparse.ArgumentParser(description="Report app sign-ins")
    parser.add_argument("--limit", type=int, default=200, help="Number of most-recent sign-ins to scan")
    args = parser.parse_args()

    client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)
    signins = client.audit_logs.signins.top(args.limit).get().execute_query()
    counts = Counter(s.app_display_name or "(unknown)" for s in signins)

    print(f"App sign-ins — top {min(15, len(counts))} of {len(signins)} sign-ins:\n")
    for app, count in counts.most_common(15):
        print(f"  {app:45s} {count}")


if __name__ == "__main__":
    main()
