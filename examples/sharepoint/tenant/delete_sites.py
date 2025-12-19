from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.tenant.administration.jobs.spo_operation import SpoOperation
from tests import test_admin_site_url, test_client_id, test_password, test_tenant, test_username

admin_client = ClientContext(test_admin_site_url).with_username_and_password(
    test_tenant, test_client_id, test_username, test_password
)


# sitesResult = admin_client.tenant.get_site_properties_from_sharepoint_by_filters("").execute_query()
sitesResult = admin_client.tenant.get_deleted_site_properties(0).execute_query()


def site_deleted(op: SpoOperation, site_url: str):
    print(f"Site '{site_url}' deleted successfully ...")


admin_client.tenant.remove_deleted_sites([r.url for r in sitesResult], success_callback=site_deleted).execute_query()


print(f"\nComplete: Processed {len(sitesResult)} sites")
