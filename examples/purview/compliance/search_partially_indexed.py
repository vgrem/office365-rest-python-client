"""
Run a compliance search for partially indexed items across SharePoint
and Exchange.

Partially indexed items (unsupported file types, encryption, or
indexing failures) are invisible to normal searches but can hold
relevant content for eDiscovery. This example runs a compliance
search and reports items that couldn't be fully indexed.

Inspired by ComplianceSearchPartiallyIndexedItems.ps1 from
Office 365 for IT Pros.

Required delegated permissions (Security & Compliance):
    eDiscovery.Read.All          Read compliance searches
    eDiscovery.ReadWrite.All     Create compliance searches

https://learn.microsoft.com/en-graph/api/resources/security-ediscoverysearch
"""

from office365.graph_client import GraphClient
from tests import test_client_id, test_client_secret, test_tenant


def run_compliance_search(name: str, query: str) -> dict:
    """Create and run a compliance search for partially indexed items.

    Args:
        name: Display name for the search.
        query: Search query (KQL format — can use * for all content).

    Returns:
        Search result summary with hit and partially indexed counts.
    """
    client = GraphClient(tenant=test_tenant).with_client_secret(
        test_client_id, test_client_secret
    )

    # Create eDiscovery case for the search
    case = client.security.cases.ediscovery_cases.add(
        display_name=f"Compliance scan — {name}"
    ).execute_query()

    search = client.security.cases.ediscovery_cases[case.id].searches.add(
        display_name=name,
        content_query=query,
        data_source_scopes="allTenantMailboxes,allTenantSites",
    ).execute_query()

    # Estimate the search results (kicks off the search)
    estimate = search.estimate_statistics().execute_query()

    return {
        "id": search.id,
        "name": name,
        "query": query,
        "status": getattr(estimate, "status", "Unknown"),
        "estimated_hits": getattr(estimate, "estimated_hits_count", 0),
        "partially_indexed": getattr(estimate, "estimated_partially_indexed_item_count", 0),
        "mailbox_count": getattr(estimate, "estimated_mailbox_count", 0),
        "site_count": getattr(estimate, "estimated_site_count", 0),
    }


def main():
    print("Running compliance search for partially indexed items...\n")

    # Search all content — we're interested in the partially indexed stats
    result = run_compliance_search(
        name="Partially indexed items scan",
        query="*",
    )

    print(f"Search:              {result['name']}")
    print(f"Query:               {result['query']}")
    print(f"Status:              {result['status']}")
    print(f"Estimated hits:      {result['estimated_hits']}")
    print(f"Mailbox sources:     {result['mailbox_count']}")
    print(f"Site sources:        {result['site_count']}")
    print(f"\nPartially indexed items: {result['partially_indexed']}")

    if result["partially_indexed"] > 0:
        print("\nPartially indexed items may contain relevant content")
        print("not captured in normal searches. Consider reviewing them")
        print("via the Microsoft Purview compliance portal.")


if __name__ == "__main__":
    main()
