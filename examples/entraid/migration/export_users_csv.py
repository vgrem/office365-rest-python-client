"""
Export users to CSV — full user inventory for migration planning.

Exports key user properties to a CSV file for integration with
migration tools, HR systems, or audit reporting.

Fields: UPN, display name, given name, surname, department, job
title, office location, city, country, mobile/phone, enabled
status, mail, MFA registered, creation date, last sign-in date,
assigned license SKUs.

Requires delegated permission ``User.Read.All``,
``Organization.Read.All``, ``AuditLog.Read.All`` (for last sign-in),
``UserAuthenticationMethod.Read.All`` (for MFA status).

https://learn.microsoft.com/en-us/graph/api/user-list
"""

import csv

from office365.graph_client import GraphClient
from tests import test_client_id, test_client_secret, test_tenant

OUTPUT_FILE = "/tmp/users_export.csv"
FIELDS = [
    "userPrincipalName",
    "displayName",
    "givenName",
    "surname",
    "department",
    "jobTitle",
    "officeLocation",
    "city",
    "country",
    "mobilePhone",
    "businessPhones",
    "mail",
    "accountEnabled",
    "userType",
    "createdDateTime",
    "signInActivity",
    "assignedLicenses",
]


def get_license_skus(client: GraphClient) -> dict:
    """Map SKU IDs to human-readable names."""
    skus = client.subscribed_skus.get().execute_query()
    return {s.sku_id: s.sku_part_number for s in skus if hasattr(s, "sku_id") and hasattr(s, "sku_part_number")}


def get_mfa_status(client: GraphClient) -> dict[str, dict]:
    """Get MFA and passwordless registration status per user."""
    try:
        details = client.reports.authentication_methods.user_registration_details.get().execute_query()
        return {d.user_principal_name.upper(): d for d in details}
    except Exception:
        return {}


def main():
    client = GraphClient(tenant=test_tenant).with_client_secret(test_client_id, test_client_secret)

    print("Fetching users...")
    users = client.users.get_all().execute_query()
    print(f"  Found {len(users)} users")

    sku_map = get_license_skus(client)
    mfa_map = get_mfa_status(client)
    print(f"  Resolved {len(sku_map)} license SKUs")

    with open(OUTPUT_FILE, "w", newline="") as f:
        writer = csv.DictWriter(
            f, fieldnames=FIELDS + ["licenseSkus", "mfaRegistered", "passwordlessCapable", "lastSignIn"]
        )
        writer.writeheader()

        for u in users:
            upn = u.user_principal_name or ""
            mfa = mfa_map.get(upn.upper())
            last_signin = u.properties.get("signInActivity")
            if hasattr(last_signin, "last_sign_in_date_time"):
                last_signin = last_signin.last_sign_in_date_time
            else:
                last_signin = u.properties.get("signInActivity/lastSignInDateTime", "")

            licenses = []
            if u.assigned_licenses:
                for lic in u.assigned_licenses:
                    sku_id = lic.properties.get("skuId", "")
                    licenses.append(sku_map.get(sku_id, sku_id))

            writer.writerow(
                {
                    "userPrincipalName": upn,
                    "displayName": u.display_name or "",
                    "givenName": u.given_name or "",
                    "surname": u.surname or "",
                    "department": u.department or "",
                    "jobTitle": u.job_title or "",
                    "officeLocation": u.office_location or "",
                    "city": u.city or "",
                    "country": u.country or "",
                    "mobilePhone": u.mobile_phone or "",
                    "businessPhones": ", ".join(u.business_phones) if u.business_phones else "",
                    "mail": u.mail or "",
                    "accountEnabled": u.account_enabled,
                    "userType": u.user_type or "",
                    "createdDateTime": u.created_date_time.strftime("%Y-%m-%d") if u.created_date_time else "",
                    "signInActivity": str(last_signin)[:10] if last_signin else "",
                    "assignedLicenses": ";".join(licenses) if licenses else "",
                    "licenseSkus": ";".join(licenses) if licenses else "",
                    "mfaRegistered": str(mfa.is_mfa_registered) if mfa else "",
                    "passwordlessCapable": str(mfa.is_passwordless_capable) if mfa else "",
                    "lastSignIn": str(last_signin)[:10] if last_signin else "",
                }
            )

    print(f"\n✓ Exported {len(users)} users to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
