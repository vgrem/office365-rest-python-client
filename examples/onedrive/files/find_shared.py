"""
Sharing audit — find files shared via links.

Governance check: which files in a drive are exposed through sharing links
(anonymous or organization-wide). Detects oversharing and confirms who has
access.

Requires delegated permission ``Files.Read.All``.

https://learn.microsoft.com/en-us/graph/api/permission-list
"""

import argparse

from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant


def main():
    parser = argparse.ArgumentParser(description="Audit files shared via links in a drive")
    parser.add_argument("--max-files", type=int, default=100, help="max files to inspect (default: 100)")
    args = parser.parse_args()

    client = (
        GraphClient(tenant=tenant)
        .with_client_secret(client_id, client_secret)
        .require_application_permission("Files.Read.All", "Sites.Read.All")
    )

    files = list(client.me.drive.root.get_files(recursive=True).execute_query())[: args.max_files]

    shared = 0
    print(f"Scanning {len(files)} files for sharing links...\n")
    for f in files:
        permissions = f.permissions.get().execute_query()
        links = [p for p in permissions if p.link]
        if not links:
            continue
        shared += 1
        scope = ", ".join(p.link.scope or "?" for p in links)
        print(f"  {f.name:40s}  scope: {scope}")
        for p in links:
            if p.link.webUrl:
                print(f"      {p.link.webUrl}")

    print(f"\n{shared} of {len(files)} files are shared via links.")


if __name__ == "__main__":
    main()
