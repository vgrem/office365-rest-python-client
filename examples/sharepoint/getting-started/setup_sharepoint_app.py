"""Set up certificate (app-only) access to SharePoint Online, end to end.

Reuses an existing app registration (or creates one with ``--new-app``), attaches
a self-signed certificate, grants the SharePoint **application permission** with
admin consent, grants the app access to each target site, and writes the
connection values to ``.env``.

Requires Global Administrator or Privileged Role Administrator, plus the
delegated ``Application.ReadWrite.All`` permission on the sign-in app. The full
walkthrough is in ``getting-started/README.md``.

https://learn.microsoft.com/en-us/sharepoint/dev/solution-guidance/security-apponly-azuread
"""

from __future__ import annotations

import argparse
import shutil
import sys

from office365.directory.applications.app_ids import MsAppIds
from office365.directory.applications.application import Application
from office365.graph_client import GraphClient
from tests.settings import settings
from tests.setup import (
    CERT_PRIVATE,
    CERT_PUBLIC,
    ENV_BAK,
    ENV_PATH,
    PROJECT_ROOT,
    generate_certificate,
    merge_env,
)

SITES_SELECTED = "Sites.Selected"
SITES_FULL_CONTROL = "Sites.FullControl.All"
SITE_ROLES = ("read", "write", "manage", "fullcontrol")


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Set up certificate app-only access to SharePoint Online.")
    parser.add_argument(
        "--site", action="append", default=[], metavar="URL", help="site to grant access to (repeatable)"
    )
    parser.add_argument(
        "--scope",
        choices=["selected", "all"],
        default="selected",
        help="'selected': Sites.Selected + one grant per --site; 'all': Sites.FullControl.All tenant-wide",
    )
    parser.add_argument(
        "--role",
        choices=SITE_ROLES,
        default="write",
        help="per-site role for '--scope selected' (default: write)",
    )
    parser.add_argument("--new-app", action="store_true", help="create an app instead of reusing OFFICE365_CLIENT_ID")
    parser.add_argument("--app-name", default="sharepoint-app", help="display name for --new-app and the certificate")
    parser.add_argument("--force-cert", action="store_true", help="regenerate the local certificate even if one exists")
    parser.add_argument("--interactive", action="store_true", help="browser sign-in instead of the device code flow")
    parser.add_argument("--no-write", action="store_true", help="print the connection values but do not touch .env")
    parser.add_argument("--tenant", help="tenant domain or id (default: OFFICE365_TENANT)")
    parser.add_argument("--client-id", dest="client_id", help="sign-in / target app id (default: OFFICE365_CLIENT_ID)")
    parser.add_argument("--admin", help="admin UPN for interactive sign-in (default: OFFICE365_ADMIN_USERNAME)")
    return parser.parse_args()


def _require_openssl() -> None:
    if shutil.which("openssl") is None:
        sys.exit("openssl is required to generate the certificate; install it and retry.")


def _sign_in(tenant: str, client_id: str, admin: str, interactive: bool) -> GraphClient:
    client = GraphClient(tenant=tenant)
    client = client.with_token_interactive(client_id, admin) if interactive else client.with_device_flow(client_id)
    try:
        client.require_role("Global Administrator", "Privileged Role Administrator")
    except SystemExit:
        print("Continuing without verifying the admin role.")
    return client


def _ensure_app(client: GraphClient, client_id: str, app_name: str, new_app: bool) -> Application:
    app = client.applications.ensure(
        app_name, None if new_app else client_id, create_service_principal=True
    ).execute_query()
    if new_app:
        print(f"Created app '{app.display_name}' ({app.app_id})")
    return app


def _ensure_certificate(app, app_name: str, force: bool) -> str:
    if force or not (CERT_PUBLIC.is_file() and CERT_PRIVATE.is_file()):
        _require_openssl()
        generate_certificate(app_name)
        print(f"Generated {CERT_PUBLIC.relative_to(PROJECT_ROOT)}")
    app.ensure_certificate(CERT_PUBLIC, app_name).execute_query()
    print(f"Ensured the certificate on app {app.app_id}.")
    return Application.certificate_thumbprint(CERT_PUBLIC)


def _grant_app_permission(client: GraphClient, app_id: str, scope: str) -> None:
    resource = client.service_principals.get_by_app_id(MsAppIds.Office_365_SharePoint_Online)
    granted = resource.get_application_permissions(app_id).execute_query().value
    if any(role.value == scope for role in granted):
        print(f"'{scope}' is already granted.")
        return
    resource.grant_application_permissions(app_id, scope)
    client.execute_query()
    print(f"Granted '{scope}' with admin consent.")


def _write_env(tenant: str, app_id: str, thumbprint: str, sites: list[str], write: bool) -> None:
    overrides = {
        "OFFICE365_TENANT": tenant,
        "OFFICE365_CLIENT_ID": app_id,
        "OFFICE365_CERT_THUMBPRINT": thumbprint,
        "OFFICE365_CERT_PATH": CERT_PRIVATE.relative_to(PROJECT_ROOT).as_posix(),
    }
    defaults: dict[str, str] = {}
    if sites:
        defaults["OFFICE365_SITE_URL"] = sites[0]
        defaults["OFFICE365_TEAM_SITE_URL"] = sites[0]
    print()
    print("Connection values:")
    for key, value in overrides.items():
        print(f"  {key}={value}")
    if not write:
        print("\n(.env not updated; re-run without --no-write to apply)")
        return
    if ENV_PATH.is_file():
        shutil.copy2(ENV_PATH, ENV_BAK)
    ENV_PATH.write_text(merge_env(overrides, defaults), encoding="utf-8")
    print(f"\nUpdated {ENV_PATH.relative_to(PROJECT_ROOT)}")


def main() -> int:
    args = _parse_args()
    tenant = args.tenant or settings.tenant
    client_id = args.client_id or settings.client_id
    admin = args.admin or settings.admin_username

    if not tenant or not client_id:
        sys.exit("Set OFFICE365_TENANT and OFFICE365_CLIENT_ID (or pass --tenant/--client-id).")
    if args.interactive and not admin:
        sys.exit("Interactive sign-in needs an admin UPN (--admin or OFFICE365_ADMIN_USERNAME).")
    if args.scope == "selected" and not args.site:
        sys.exit("Pass at least one --site (or use --scope all for a tenant-wide grant).")

    client = _sign_in(tenant, client_id, admin, args.interactive)
    app = _ensure_app(client, client_id, args.app_name, args.new_app)
    thumbprint = _ensure_certificate(app, args.app_name, args.force_cert)

    scope = SITES_FULL_CONTROL if args.scope == "all" else SITES_SELECTED
    _grant_app_permission(client, app.app_id, scope)
    if args.scope == "selected":
        for site_url in args.site:
            site = client.sites.get_by_url(site_url).get().execute_query()
            site.grant_app_access(app.app_id, args.role).execute_query()
            print(f"Granted '{args.role}' to the app on {site_url}.")

    _write_env(tenant, app.app_id, thumbprint, args.site, not args.no_write)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (EOFError, KeyboardInterrupt):
        print("\nAborted.")
        raise SystemExit(130) from None
