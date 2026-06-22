"""
Access reviews — list history definitions, instances, and decisions.

Requires delegated permission ``AccessReview.Read.All`` or
``AccessReview.ReadWrite.All``.

https://learn.microsoft.com/en-us/graph/api/resources/accessreviewsv2-overview
"""

from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant


def main():
    client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)

    ar = client.identity_governance.access_reviews

    hist_defs = ar.history_definitions.get().execute_query()
    print(f"History definitions: {len(hist_defs)}\n")

    for hd in hist_defs:
        created_by = hd.created_by.user_principal_name if hd.created_by else "?"
        print(f"  {hd.display_name:35s}  status={hd.status.name if hd.status else '?'}  created_by={created_by}")
        for inst in hd.instances.get().execute_query() or []:
            dt = inst.created_date_time.strftime("%Y-%m-%d") if inst.created_date_time else "?"
            print(f"    -> instance: created={dt}  status={inst.properties.get('status', '?')}")

    if not hist_defs:
        print("(No history definitions found.)")

    print("\nDirect API call to list schedule definitions:")
    try:
        response = client.execute_request_get(
            "/identityGovernance/accessReviews/definitions?$select=id,displayName,status,createdDateTime&$top=10"
        )
        for d in response.json().get("value", []):
            print(
                f"    {d.get('displayName', '?'):40s}  status={d.get('status', '?'):15s}  "
                f"created={str(d.get('createdDateTime', ''))[:10]}"
            )
    except Exception as e:
        print(f"  (not available: {e})")


if __name__ == "__main__":
    main()
