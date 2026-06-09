"""
Access reviews — list review history definitions, instances, and
decisions.

Access reviews are a core identity governance feature for certifying
that users still need access to groups, apps, and roles.

This example focuses on what the SDK exposes via the
``access_reviews`` navigation path:
  - List history definitions (one-time or recurring export jobs)
  - Show instances and their status
  - Show decisions per instance

For creating ad-hoc access review schedule definitions, use the Graph
API endpoint ``POST /identityGovernance/accessReviews/definitions``.

Requires delegated permission ``AccessReview.Read.All`` or
``AccessReview.ReadWrite.All``.

https://learn.microsoft.com/en-us/graph/api/resources/accessreviewsv2-overview
"""

from office365.graph_client import GraphClient
from tests import test_client_id, test_client_secret, test_tenant


def main():
    client = GraphClient(tenant=test_tenant).with_client_secret(test_client_id, test_client_secret)

    ar = client.identity_governance.access_reviews

    # -- Step 1: access review history definitions (compliance exports) --
    hist_defs = ar.history_definitions.get().execute_query()
    print(f"History definitions: {len(hist_defs)}\n")

    for hd in hist_defs:
        created_by = getattr(hd.created_by, "user_principal_name", "?") if hd.created_by else "?"
        print(f"  {hd.display_name:35s}  status={hd.status.name if hd.status else '?':12s}  "
              f"created_by={created_by:30s}  "
              f"period={str(hd.review_history_period_start_date_time)[:10] or '?'} → {str(hd.review_history_period_end_date_time)[:10] or '?'}")

        # Enumerate instances
        instances = hd.instances.get().execute_query()
        for inst in instances:
            dt_str = inst.created_date_time.strftime("%Y-%m-%d %H:%M") if inst.created_date_time else "?"
            print(f"    ↳ instance: created={dt_str}  status={inst.status if hasattr(inst, 'status') else '?'}")

    # -- Step 2: if no history definitions exist, show how to create one --
    if not hist_defs:
        print("(No history definitions found.)")
        print()
        print("To generate an access review history report:")
        print("""  from office365.directory.identitygovernance.accessreview.history.definition import AccessReviewHistoryDefinition
  from office365.directory.identitygovernance.accessreview.scope import AccessReviewScope
  from office365.directory.identitygovernance.accessreview.history.decisionfilter import AccessReviewHistoryDecisionFilter

  definition = AccessReviewHistoryDefinition(client.context)
  definition.set_property("displayName", "Q1 Access Review History")
  definition.set_property("scopes", [AccessReviewScope()])
  definition.set_property("decisions", [AccessReviewHistoryDecisionFilter.approve])
  ar.history_definitions.add_child(definition)
  client.execute_query()
""")

    # -- Step 3: enumerate access reviews directly via the definitions endpoint --
    # The SDK doesn't expose definitions as a navigation property yet.
    # Use the Graph API directly via the SDK's underlying client:
    print("\nDirect API call to list schedule definitions:")
    try:
        response = client.execute_request_get(
            "/identityGovernance/accessReviews/definitions"
            "?$select=id,displayName,status,createdDateTime"
            "&$top=10"
        )
        definitions = response.json().get("value", [])
        print(f"  Schedule definitions: {len(definitions)}")
        for d in definitions:
            print(f"    {d.get('displayName','?'):40s}  status={d.get('status','?'):15s}  "
                  f"created={str(d.get('createdDateTime',''))[:10]}")
    except Exception as e:
        print(f"  (not available: {e})")


if __name__ == "__main__":
    main()
