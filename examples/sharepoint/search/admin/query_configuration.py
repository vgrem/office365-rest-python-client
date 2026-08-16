"""
Search administration — query configuration and promoted results (best bets).

Requires delegated permission ``Sites.ReadWrite.All``.

https://learn.microsoft.com/en-us/sharepoint/dev/general-development/search-in-sharepoint
"""

from office365.sharepoint.client_context import ClientContext
from tests.settings import cert_path, cert_thumbprint, client_id, site_url, tenant


def main():
    ctx = ClientContext(site_url).with_client_certificate(
        tenant, client_id=client_id, thumbprint=cert_thumbprint, cert_path=cert_path
    )

    # 1. Query configuration (search schema / result types settings)
    config = ctx.search_setting.get_query_configuration().execute_query().value
    print("Query configuration:")
    print(f"  Query endpoint: {config.SearchEndpoints.QueryEndpoint or '?'}")
    print(f"  Admin endpoint: {config.SearchEndpoints.AdminEndpoint or '?'}")
    print()

    # 2. Promoted results (best bets) at tenant level
    promoted = (
        ctx.search_setting.get_promoted_result_query_rules(site_collection_level=False, number_of_rules=10)
        .execute_query()
        .value
    )
    rules = promoted.Result
    print(f"Promoted results (best bets) — {len(rules)}:")
    for rule in rules:
        title = rule.DisplayName or rule.Contact or "(unnamed)"
        promoted_count = len(rule.PromotedResults) if rule.PromotedResults else 0
        print(f"  {title:35s}  promoted results: {promoted_count}")


if __name__ == "__main__":
    main()
