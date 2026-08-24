"""
List MFA registration status for all users.

Shows which users have MFA registered, their authentication methods, and a
tenant-wide summary of MFA coverage.

Requires delegated permission ``AuditLog.Read.All`` or ``Reports.Read.All``.

https://learn.microsoft.com/en-us/graph/api/authenticationmethods-list-userregistrationdetails
"""

import argparse

from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant


def main():
    parser = argparse.ArgumentParser(description="Report MFA registration status for users")
    parser.add_argument("--unregistered-only", action="store_true", help="only list users without MFA registered")
    args = parser.parse_args()

    client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)
    result = client.reports.authentication_methods.user_registration_details.get().execute_query()

    total = len(result)
    registered = 0
    print(f"{'User':40s}  {'MFA':6s}  {'Methods'}")
    print("-" * 90)
    for details in result:
        is_registered = bool(details.is_mfa_registered)
        if is_registered:
            registered += 1
        if args.unregistered_only and is_registered:
            continue
        methods = ", ".join(details.properties.get("methods", []) or [])
        print(f"{details.user_principal_name:40s}  {str(is_registered):6s}  {methods}")

    pct = registered / total * 100 if total else 0.0
    print(f"\n{registered} of {total} users have MFA registered ({pct:.1f}%)")


if __name__ == "__main__":
    main()
