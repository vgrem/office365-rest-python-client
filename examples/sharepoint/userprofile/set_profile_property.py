"""
Set a user profile property (single- or multi-valued).

Example property names: ``SPS-Skills`` (multi-valued), ``SPS-Location``,
``AboutMe``, ``Department``.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/people-rest-api
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import cert_path, cert_thumbprint, client_id, site_url, tenant


def main():
    parser = argparse.ArgumentParser(description="Set a user profile property")
    parser.add_argument("--user", default=None, help="Account name of the user (default: current user)")
    parser.add_argument("--property", required=True, help="Profile property name, e.g. SPS-Skills")
    parser.add_argument("--value", help="Value for a single-valued property")
    parser.add_argument("--values", nargs="+", help="Values for a multi-valued property")
    parser.add_argument("--commit", action="store_true", help="Actually commit (default: dry-run)")
    args = parser.parse_args()

    if not args.value and not args.values:
        raise SystemExit("Provide --value (single) or --values (multi)")

    ctx = ClientContext(site_url).with_client_certificate(
        tenant, client_id=client_id, thumbprint=cert_thumbprint, cert_path=cert_path
    )
    account_name = args.user
    if not account_name:
        me = ctx.web.current_user
        account_name = me.login_name
    if not account_name:
        raise SystemExit("Account name could not be resolved")

    if not args.commit:
        print(f"[dry-run] would set '{args.property}' = {args.value or args.values} on {account_name}")
        return

    if args.values:
        ctx.people_manager.set_multi_valued_profile_property(account_name, args.property, args.values)
    else:
        ctx.people_manager.set_single_value_profile_property(account_name, args.property, args.value)
    ctx.execute_query()
    print(f"Set '{args.property}' = {args.value or args.values} on {account_name}")


if __name__ == "__main__":
    main()
