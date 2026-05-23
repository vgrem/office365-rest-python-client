"""
Application Lifecycle Management (ALM) for SharePoint Framework (SPFx) solutions.

Official docs:
  https://learn.microsoft.com/en-us/sharepoint/dev/apis/alm-api-for-spfx-add-ins
"""

import os

from office365.sharepoint.client_context import ClientContext
from tests import (
    test_admin_site_url,
    test_client_id,
    test_team_site_url,
    test_tenant,
)

# ── Customize ─────────────────────────────────────────────
SPPKG_PATH = f"{os.path.dirname(__file__)}/react-banner.sppkg"
APP_TITLE = "Starter Kit - Banner"
# ──────────────────────────────────────────────────────────


if __name__ == "__main__":
    # admin = ClientContext(test_admin_site_url).with_client_credentials(test_client_id, test_client_secret)
    admin = ClientContext(test_admin_site_url).with_interactive(test_tenant, test_client_id)
    catalog = admin.tenant.get_corporate_catalog_site().execute_query()

    # ── 1. Upload ─────────────────────────────────────────
    # Add .sppkg to the tenant app catalog
    app_file = catalog.context.web.tenant_app_catalog.app_from_path(SPPKG_PATH, True).execute_query()
    print(f"✅ Uploaded: {app_file.name}")

    # ── 2. List ───────────────────────────────────────────
    # List all apps in the catalog
    apps = catalog.context.web.tenant_app_catalog.available_apps.get().execute_query()
    for app in apps:
        print(f"  • {app.title}  (ID: {app.id})")
    print(f"Total: {len(apps)} app(s)")

    # ── 3. Inspect ────────────────────────────────────────
    # Get metadata and check upgrade availability
    app = catalog.context.web.tenant_app_catalog.available_apps.get_by_title(APP_TITLE).execute_query()
    assert app.id is not None
    # upgrade_result = admin.web.tenant_app_catalog.is_app_upgrade_available(app.id).execute_query()
    # upgrade_avail = upgrade_result.value.IsUpgradeAvailable
    # print(
    #    f"Title: {app.title} | Version: {app.app_catalog_version} | "
    #    f"Can upgrade: {app.can_upgrade} | Upgrade avail: {upgrade_avail}"
    # )

    # ── 4. Deploy ─────────────────────────────────────────
    # Approve the app for installation
    app.deploy(skip_feature_deployment=False).execute_query()
    print(f"✅ Deployed: {app.title}")

    # ── 5. Install ────────────────────────────────────────
    # Install on a target site (runs on the catalog web context)
    app_on_site = catalog.context.web.tenant_app_catalog.available_apps.get_by_title(APP_TITLE).execute_query()
    app_on_site.install().execute_query()
    print(f"✅ Installed: {app.title} on {test_team_site_url}")

    # ── 6. Upgrade ────────────────────────────────────────
    # Deploy a newer version from the catalog, then install on the site
    if app.can_upgrade:
        app.deploy(skip_feature_deployment=False).execute_query()
        app_on_site = catalog.context.web.tenant_app_catalog.available_apps.get_by_title(APP_TITLE).execute_query()
        app_on_site.install().execute_query()
        print(f"✅ Upgraded: {app.title}")

    # ── 7. Uninstall ──────────────────────────────────────
    # Remove from the target site
    app_on_site = catalog.context.web.tenant_app_catalog.available_apps.get_by_title(APP_TITLE).execute_query()
    app_on_site.uninstall().execute_query()
    print(f"✅ Uninstalled: {app.title} from {test_team_site_url}")

    # ── 8. Remove ────────────────────────────────────────
    # Delete from the app catalog entirely
    app.remove().execute_query()
    print(f"✅ Removed: {app.title} from catalog")
