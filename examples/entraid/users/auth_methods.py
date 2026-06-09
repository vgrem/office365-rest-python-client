"""
Authentication methods — audit registered methods per user and check
tenant-wide passwordless / MFA / SSPR readiness.

Shows three perspectives:
  1. Tenant-wide summary: users registered by method and by feature.
  2. Per-user detail: which methods each user has registered and what
     they're capable of (MFA, passwordless, SSPR).
  3. Per-user authentication methods: FIDO2 keys, Microsoft
     Authenticator, phone, password.

Useful for MFA roll-out tracking, passwordless adoption reporting,
and security compliance audits.

Requires delegated permission ``UserAuthenticationMethod.Read.All``
and ``AuditLog.Read.All``.

https://learn.microsoft.com/en-us/graph/api/resources/authenticationmethods-overview
"""

from office365.graph_client import GraphClient
from tests import test_client_id, test_client_secret, test_tenant


def main():
    client = GraphClient(tenant=test_tenant).with_client_secret(test_client_id, test_client_secret)

    am = client.reports.authentication_methods

    # -- Step 1: tenant-wide summary by feature (MFA, SSPR, passwordless) --
    feature_summary = am.users_registered_by_feature().execute_query()
    if feature_summary and feature_summary.value:
        fs = feature_summary.value
        print("Users by authentication feature:")
        print(f"  Total users         : {fs.total_user_count}")
        print(f"  MFA registered      : {fs.mfa_registered_count or '?'}")
        print(f"  SSPR capable        : {fs.sspr_capable_count or '?'}")
        print(f"  SSPR enabled        : {fs.sspr_enabled_count or '?'}")
        print(f"  Passwordless capable: {fs.passwordless_capable_count or '?'}")
        print()

    # -- Step 2: tenant-wide summary by method --
    method_summary = am.users_registered_by_method().execute_query()
    if method_summary and method_summary.value:
        ms = method_summary.value
        print("Users by authentication method:")
        if hasattr(ms, "users_registered_by_method") and ms.users_registered_by_method:
            for m in ms.users_registered_by_method:
                print(f"  {m.method_type or '?':30s}  {m.user_count or 0} users")
        elif hasattr(ms, "registration_count") and ms.registration_count:
            for rc in ms.registration_count:
                print(f"  {rc.method or '?':30s}  {rc.count or 0} users")
        print()

    # -- Step 3: per-user registration details --
    details = am.user_registration_details.top(20).get().execute_query()
    print(f"User registration details (showing {len(details)} users):\n")
    print(f"{'UPN':35s} {'MFA':6s} {'PW-less':9s} {'SSPR-cap':9s} {'SSPR-en':8s} {'Admin':6s}  {'Preferred method'}")
    print("-" * 100)

    for d in details:
        pref = d.user_preferred_method_for_secondary_authentication or "-"
        print(
            f"{d.user_principal_name[:33]:35s} "
            f"{'✔' if d.is_mfa_registered else '✗':6s} "
            f"{'✔' if d.is_passwordless_capable else '✗':9s} "
            f"{'✔' if d.is_sspr_capable else '✗':9s} "
            f"{'✔' if d.is_sspr_enabled else '✗':8s} "
            f"{'✔' if d.is_admin else '':6s}  "
            f"{pref}"
        )

    # -- Step 4: per-user registered methods for a specific user --
    print()
    sample_upn = details[0].user_principal_name if details else "admin@contoso.onmicrosoft.com"
    users = client.users.filter(f"userPrincipalName eq '{sample_upn}'").get().execute_query()
    if users:
        user = users[0]
        auth = user.authentication
        all_methods = auth.methods.get().execute_query()
        print(f"Authentication methods for {user.user_principal_name}: {len(all_methods)}")
        for m in all_methods:
            mtype = m.properties.get("@odata.type", m.entity_type_name)
            extra = ""
            if "phone" in mtype.lower():
                extra = m.properties.get("phoneNumber", "") or m.properties.get("phoneType", "")
            elif "fido" in mtype.lower():
                extra = m.properties.get("displayName", "")
            elif "microsoftAuthenticator" in mtype.lower():
                extra = m.properties.get("displayName", "")
            print(f"  {mtype:55s}  {extra}")


if __name__ == "__main__":
    main()
