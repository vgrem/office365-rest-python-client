"""
Terms of use — list agreements and track user acceptances.

Requires delegated permission ``Agreement.Read.All`` and
``AgreementAcceptance.Read.All``.

https://learn.microsoft.com/en-us/graph/api/resources/agreement
"""

from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant


def _fmt(dt):
    return dt.strftime("%Y-%m-%d") if hasattr(dt, "strftime") else str(dt or "?")


def main():
    client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)

    tos = client.identity_governance.terms_of_use

    agreements = tos.agreements.get().execute_query()
    print(f"Terms of use agreements: {len(agreements)}\n")
    for a in agreements:
        print(f"  {a.display_name or '(unnamed)'}")
        print(
            f"    view_required={a.is_viewing_before_acceptance_required}  "
            f"per_device={a.is_per_device_acceptance_required}  "
            f"reaccept_freq={a.user_reaccept_required_frequency}"
        )

        for f in a.files.get().execute_query() or []:
            print(f"    File: {f.properties.get('fileName', '?')}")

        acceptances = a.acceptances.get().execute_query()
        users = {acc.properties.get("userPrincipalName") for acc in acceptances}
        users.discard(None)
        print(f"    Accepted by: {len(users)} user(s)")
        if users:
            for u in sorted(users)[:5]:
                print(f"      {u}")

    all_acceptances = tos.agreement_acceptances.get().execute_query()
    print(f"\nTotal acceptances: {len(all_acceptances)}")

    accepted_upns = {acc.properties.get("userPrincipalName", "").upper() for acc in all_acceptances}
    accepted_upns.discard("")

    users = client.users.select(["userPrincipalName", "displayName"]).top(100).get().execute_query()
    pending = [u for u in users if (u.user_principal_name or "").upper() not in accepted_upns]
    if pending:
        print(f"\nUsers without acceptance: {len(pending)} / {len(users)}")
        for u in pending[:5]:
            print(f"  {u.user_principal_name}  {u.display_name or ''}")


if __name__ == "__main__":
    main()
