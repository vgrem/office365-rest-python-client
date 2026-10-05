"""
Grant or revoke an app's access to specific SharePoint sites (``Sites.Selected``).

The least-privilege companion to ``getting-started/``: point it at a service
principal and a list of sites to grant per-site access, or pass ``--revoke`` to
remove it again. The plain `Sites.Selected` model keeps an app scoped to exactly
the sites you list, instead of tenant-wide ``Sites.FullControl.All``.

    # Grant write access to two sites
    python grant_app_site_access.py --app-id <client-id> \
        --site https://contoso.sharepoint.com/sites/alpha \
        --site https://contoso.sharepoint.com/sites/beta

    # Revoke it again, reading the list from a file
    python grant_app_site_access.py --app-id <client-id> --sites-file sites.txt --revoke

Requires the calling app to hold ``Sites.FullControl.All`` (application) with
admin consent; the target app must already have ``Sites.Selected`` granted.

https://learn.microsoft.com/en-us/graph/api/site-post-permissions
"""

from __future__ import annotations

import argparse
from pathlib import Path

from office365.graph_client import GraphClient
from tests.settings import cert_path, cert_thumbprint, client_id, tenant


def read_sites(args: argparse.Namespace) -> list[str]:
    """Collect site URLs from ``--site`` flags and an optional ``--sites-file``."""
    sites = list(args.site)
    if args.sites_file:
        for raw in Path(args.sites_file).expanduser().read_text(encoding="utf-8").splitlines():
            line = raw.strip()
            if line and not line.startswith("#"):
                sites.append(line)
    return list(dict.fromkeys(sites))  # de-duplicate, keep order


def main() -> None:
    parser = argparse.ArgumentParser(description="Grant or revoke an app's access to specific SharePoint sites")
    parser.add_argument("--app-id", required=True, help="application (client) ID of the target app")
    parser.add_argument("--site", action="append", default=[], metavar="URL", help="site URL (repeatable)")
    parser.add_argument("--sites-file", help="file with one site URL per line (# comments allowed)")
    parser.add_argument("--role", default="write", choices=["read", "write", "owner"], help="role to grant")
    parser.add_argument("--revoke", action="store_true", help="revoke access instead of granting it")
    parser.add_argument("--dry-run", action="store_true", help="show the plan without changing anything")
    parser.add_argument("--private-key", default=cert_path, help="PEM private key of the calling app")
    args = parser.parse_args()

    sites = read_sites(args)
    if not sites:
        parser.error("provide at least one --site or a --sites-file")

    action = "Revoke access" if args.revoke else f"Grant '{args.role}'"
    print(f"{action} on {len(sites)} site(s) for app {args.app_id}:")
    for url in sites:
        print(f"  {url}")
    if args.dry_run:
        print("\nDry run: nothing changed.")
        return

    private_key = Path(args.private_key).expanduser().read_text(encoding="utf-8")
    client = GraphClient(tenant=tenant).with_certificate(client_id, cert_thumbprint, private_key)

    sp = client.service_principals.get_by_app_id(args.app_id).get().execute_query()
    print(f"\nService principal: {sp.display_name} ({sp.id})")

    for url in sites:
        site = client.sites.get_by_url(url).get().execute_query()
        if args.revoke:
            site.revoke_access(sp).execute_query()
            print(f"  revoked  {url}")
        else:
            site.grant_access(sp, args.role).execute_query()
            print(f"  granted  {url}")

    print(f"\nDone: {len(sites)} site(s).")


if __name__ == "__main__":
    main()
