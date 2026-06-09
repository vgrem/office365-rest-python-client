"""
File version policy — manage tenant-wide version limits, expiration,
and auto-deletion settings.

Version bloat is one of the most common storage problems in SharePoint.
This example shows how to:
  - Read current tenant file version policy
  - Set version expiration and delete job options
  - Get per-library version policy settings
  - Clear the policy back to tenant defaults

Requires delegated permission ``Sites.FullControl.All``.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/tenant/SetFileVersionPolicy
"""

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.tenant.administration.tenant import Tenant
from tests import test_admin_site_url, test_client_id, test_client_secret, test_tenant

# Example library to check per-library policy (replace with actual URL)
LIBRARY_URL = "https://contoso.sharepoint.com/sites/TeamSite/Shared%20Documents"


def main():
    ctx = ClientContext(test_admin_site_url).with_client_secret(test_tenant, test_client_id, test_client_secret)
    tenant = Tenant(ctx)

    # -- Step 1: get current tenant file version policy --
    policy_result = tenant.get_file_version_policy().execute_query()
    policy_xml = policy_result.value if policy_result.value else "(empty — no custom policy set)"
    print(f"Tenant file version policy:\n{policy_xml}\n")

    # -- Step 2: set a file version policy (commented by default) --
    # The policy is defined as XML. A typical policy:
    #
    # <FileVersionPolicy>
    #   <MajorVersionLimit>500</MajorVersionLimit>
    #   <MajorWithMinorVersionsLimit>500</MajorWithMinorVersionsLimit>
    #   <Expiration>
    #     <Interval>180</Interval>
    #     <DeleteAfter>AfterInterval</DeleteAfter>
    #   </Expiration>
    #   <DeleteJobInterval>7</DeleteJobInterval>
    # </FileVersionPolicy>
    #
    # MajorVersionLimit:      max major versions kept (0 = unlimited)
    # MajorWithMinorVersionsLimit: max versions including minors
    # Expiration.Interval:    delete versions older than N days
    # Expiration.DeleteAfter: "AfterInterval" or "Never"
    # DeleteJobInterval:      how often the timer job runs (days)

    # Uncomment to apply:
    # tenant.set_file_version_policy(policy_xml=new_policy).execute_query()
    # print("✓ Tenant file version policy updated.")

    # -- Step 3: get per-library version policy --
    try:
        from office365.sharepoint.tenant.administration.policies.list_parameters import SPOListParameters

        list_params = SPOListParameters(
            listUrl=LIBRARY_URL,
            listType="DocumentLibrary",
        )
        lib_policy = tenant.get_file_version_policy_for_library(
            site_url="https://contoso.sharepoint.com/sites/TeamSite",
            list_params=list_params,
        ).execute_query()

        if lib_policy and lib_policy.value:
            p = lib_policy.value
            print("\nLibrary file version policy:")
            print(f"  MajorVersionLimit:          {p.MajorVersionLimit}")
            print(f"  MajorWithMinorVersionsLimit: {p.MajorWithMinorVersionsLimit}")
            print(f"  Expiration interval:         {p.ExpirationInterval} days")
            print(f"  Delete after:                {p.DeleteAfter}")
    except Exception as e:
        print(f"\n  (per-library policy not available: {e})")

    # -- Step 4: clear file version policy back to defaults --
    # tenant.clear_file_version_policy().execute_query()
    # print("\n✓ File version policy cleared.")


if __name__ == "__main__":
    main()
