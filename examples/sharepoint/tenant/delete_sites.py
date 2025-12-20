"""
Demonstrates how to delete SharePoint sites from a tenant.

This example shows two approaches:
1. Batch deletion using remove_sites() or remove_deleted_sites() with callbacks
2. Sequential deletion with Microsoft 365 group handling

Note: If you encounter the error:
"This site belongs to a Microsoft 365 group. To delete the site, you must delete the group"

You must clear the group association first by calling:
    SiteProperties.set_property("ClearGroupId", True).update()

before attempting to delete the site.
"""

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.tenant.administration.jobs.spo_operation import SpoOperation
from tests import test_admin_site_url, test_client_id, test_password, test_tenant, test_username

admin_client = ClientContext(test_admin_site_url).with_username_and_password(
    test_tenant, test_client_id, test_username, test_password
)


def site_deleted(op: SpoOperation, site_url: str):
    """Callback invoked after each site is successfully deleted."""
    print(f"Site '{site_url}' deleted successfully ...")


# Example 1: Batch delete already-deleted sites from recycle bin
# sitesPropsCol = admin_client.tenant.get_deleted_site_properties(0).execute_query()
# admin_client.tenant.remove_deleted_sites([r.url for r in sitesPropsCol], success_callback=site_deleted).execute_query()

# Example 2: Batch delete active sites
sitesPropsCol = admin_client.tenant.get_site_properties_from_sharepoint_by_filters("").execute_query()
# admin_client.tenant.remove_sites([r.url for r in sitesPropsCol], success_callback=site_deleted).execute_query()

# Example 3: Batch delete sites that are already in recycle bin
# admin_client.tenant.remove_deleted_sites(
#    [r.url for r in sitesPropsCol], success_callback=site_deleted
# ).execute_query()


# Example 4: Sequential deletion with Microsoft 365 group clearing
# This approach is necessary when sites are associated with Microsoft 365 groups
for sitesProps in sitesPropsCol:

    if sitesProps.get_property("GroupId") != "00000000-0000-0000-0000-000000000000":
        # Clear the Microsoft 365 group association before deleting
        sitesProps.set_property("ClearGroupId", True).update().execute_query()

    if sitesProps.get_property("HubSiteId") != "00000000-0000-0000-0000-000000000000":
        # Unregister it first before deleting
        admin_client.tenant.unregister_hub_site(sitesProps.url).execute_query()

    # Delete the site
    admin_client.tenant.remove_site(sitesProps.url).execute_query()
    print(f"Site '{sitesProps.url}' deleted successfully ...")


print(f"\nComplete: Processed {len(sitesPropsCol)} sites")
