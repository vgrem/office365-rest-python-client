"""
File version policy — read and set tenant-wide version limits, expiration,
and auto-deletion settings.

Version bloat is one of the most common storage problems in SharePoint.

Requires delegated permission ``Sites.FullControl.All``.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/tenant/SetFileVersionPolicy
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.tenant.administration.policies.list_parameters import SPOListParameters
from office365.sharepoint.tenant.administration.tenant import Tenant
from tests.settings import admin_site_url, cert_path, cert_thumbprint, client_id, site_url, tenant


def main():
    parser = argparse.ArgumentParser(description="Read or set the file version policy")
    parser.add_argument("--site-url", default=site_url, help="Site URL for the per-library policy")
    parser.add_argument("--library-id", help="List/library GUID for the per-library policy")
    parser.add_argument("--set", action="store_true", help="Apply a file version policy")
    parser.add_argument("--auto-trim", type=bool, default=True, help="Trim old versions automatically")
    parser.add_argument("--major-limit", type=int, default=500, help="Max major versions to retain")
    parser.add_argument("--expire-days", type=int, default=180, help="Delete versions older than N days")
    parser.add_argument("--clear", action="store_true", help="Clear the policy back to tenant defaults")
    args = parser.parse_args()

    ctx = ClientContext(admin_site_url).with_client_certificate(
        tenant, client_id=client_id, thumbprint=cert_thumbprint, cert_path=cert_path
    )
    tenant_obj = Tenant(ctx)

    # -- Step 1: get current tenant file version policy --
    policy_result = tenant_obj.get_file_version_policy().execute_query()
    policy_xml = policy_result.value if policy_result.value else "(empty — no custom policy set)"
    print(f"Tenant file version policy:\n{policy_xml}\n")

    # -- Step 2: set a file version policy --
    if args.set:
        tenant_obj.set_file_version_policy(
            is_auto_trim_enabled=args.auto_trim,
            major_version_limit=args.major_limit,
            expire_versions_after_days=args.expire_days,
        ).execute_query()
        print("Tenant file version policy updated.\n")

    # -- Step 3: get per-library file version policy --
    if args.library_id:
        list_params = SPOListParameters(Id=args.library_id)
        lib_policy = tenant_obj.get_file_version_policy_for_library(
            site_url=args.site_url, list_params=list_params
        ).execute_query()
        if lib_policy and lib_policy.value:
            p = lib_policy.value
            print("Library file version policy:")
            print(f"  MajorVersionLimit:            {p.MajorVersionLimit}")
            print(f"  MajorWithMinorVersionsLimit:  {p.MajorWithMinorVersionsLimit}")
            print(f"  ExpireVersionsAfterDays:      {p.ExpireVersionsAfterDays}")
            print(f"  EnableAutoExpirationVersionTrim: {p.EnableAutoExpirationVersionTrim}")
        else:
            print("(per-library policy not set)")

    # -- Step 4: clear the file version policy --
    if args.clear:
        tenant_obj.clear_file_version_policy().execute_query()
        print("File version policy cleared.")


if __name__ == "__main__":
    main()
