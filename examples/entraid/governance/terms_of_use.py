"""
Terms of use — list agreements and track user acceptances.

Microsoft Entra Terms of Use lets organizations present legal
disclaimers or policy documents to users. This example shows how to:
  - List all agreements configured in the tenant
  - Check acceptance status per user
  - Track who has (and hasn't) accepted each agreement

Compliance and HR teams use this for onboarding audits and
acceptance tracking.

Requires delegated permission ``Agreement.Read.All`` and
``AgreementAcceptance.Read.All``.

https://learn.microsoft.com/en-us/graph/api/resources/agreement
"""

from office365.graph_client import GraphClient
from tests import test_client_id, test_client_secret, test_tenant

_DISPLAY_LIMIT = 5


def main():
    client = GraphClient(tenant=test_tenant).with_client_secret(test_client_id, test_client_secret)

    tos = client.identity_governance.terms_of_use

    # -- Step 1: list all agreements --
    agreements = tos.agreements.get().execute_query()
    print(f"Terms of use agreements: {len(agreements)}\n")

    for a in agreements:
        display_name = a.display_name or "(unnamed)"
        required = a.is_viewing_before_acceptance_required
        per_device = a.is_per_device_acceptance_required
        reaccept = a.user_reaccept_required_frequency

        print(f"  {display_name:45s}  view_required={required}  per_device={per_device}  reaccept_freq={reaccept}")

        # Count acceptances
        try:
            acceptances = a.acceptances.get().execute_query()
            accepted_users = set()
            for acc in acceptances:
                if acc.properties.get("userPrincipalName"):
                    accepted_users.add(acc.properties["userPrincipalName"])

            print(f"    Accepted by: {len(accepted_users)} user(s)")
            if accepted_users:
                for u in list(accepted_users)[:_DISPLAY_LIMIT]:
                    print(f"      {u}")
                if len(accepted_users) > _DISPLAY_LIMIT:
                    print(f"      … and {len(accepted_users) - _DISPLAY_LIMIT} more")
        except Exception:
            print("    (acceptances not accessible)")

        # Show agreement download link
        try:
            files = a.files.get().execute_query()
            for f in files:
                file_name = f.properties.get("fileName", "?")
                print(f"    File: {file_name}")
        except Exception:
            pass

        print()

    # -- Step 2: list all agreement acceptances tenant-wide --
    all_acceptances = tos.agreement_acceptances.get().execute_query()
    print(f"Total agreement acceptances across all agreements: {len(all_acceptances)}")

    for acc in all_acceptances[:10]:
        agreement_id = acc.properties.get("agreementId", "?")[:20]
        user_name = acc.properties.get("userPrincipalName", acc.properties.get("userDisplayName", "?"))
        recorded = acc.properties.get("recordedDateTime", "?")
        if hasattr(recorded, "strftime"):
            recorded = recorded.strftime("%Y-%m-%d")
        state = acc.properties.get("state", "?")
        print(f"  {user_name:35s}  agreement={agreement_id}  state={state}  recorded={recorded}")

    # -- Step 3: users who have NOT accepted (compliance check) --
    if agreements:
        print("\n--- Compliance check: acceptance status ---")
        users = client.users.get().select(["id", "userPrincipalName", "displayName"]).top(100).execute_query()
        accepted_upns = set()
        for acc in all_acceptances:
            upn = acc.properties.get("userPrincipalName", "")
            if upn:
                accepted_upns.add(upn.upper())

        users_without = [u for u in users if (u.user_principal_name or "").upper() not in accepted_upns]
        if users_without:
            print(f"Users without acceptance: {len(users_without)} out of {len(users)}")
            for u in users_without[:_DISPLAY_LIMIT]:
                print(f"  {u.user_principal_name:35s}  {u.display_name or ''}")
            if len(users_without) > _DISPLAY_LIMIT:
                print(f"  … and {len(users_without) - _DISPLAY_LIMIT} more")


if __name__ == "__main__":
    main()
