"""
Search administration — crawl diagnostics, popular queries, search
service configuration, and manual suggestions.

Provides search admins with tools to:
  - Check search service configuration (search center URL, result URL)
  - View crawl status and unsuccessful URLs
  - Export popular tenant queries
  - Export and update manual query suggestions

Requires delegated permission ``Sites.ReadWrite.All`` for most
operations; ``Sites.FullControl.All`` for configuration updates.

https://learn.microsoft.com/en-us/sharepoint/dev/general-development/search-in-sharepoint
"""

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.search.administration.document_crawl_log import DocumentCrawlLog
from tests import test_client_id, test_client_secret, test_site_url, test_tenant


def main():
    ctx = ClientContext(test_site_url).with_client_secret(test_tenant, test_client_id, test_client_secret)

    search_svc = ctx.search

    # -- Step 1: query search service configuration --
    center_url = search_svc.search_center_url().execute_query()
    result_url = search_svc.results_page_address().execute_query()

    print("Search service configuration:\n")
    print(f"  Search center URL:   {center_url.value or '(not set)'}")
    print(f"  Results page address: {result_url.value or '(default)'}\n")

    # -- Step 2: export popular tenant queries --
    popular = search_svc.export_popular_tenant_queries(count=10).execute_query()
    if popular and popular.value:
        print(f"Popular tenant queries (top {len(popular.value)}):")
        for i, q in enumerate(popular.value, 1):
            query_text = q.properties.get("queryText", q.properties.get("QueryText", "?"))
            count_val = q.properties.get("count", q.properties.get("Count", "?"))
            print(f"  {i:2d}. {query_text:45s}  count={count_val}")
    else:
        print("(No popular tenant query data available)")
    print()

    # -- Step 3: export manual query suggestions --
    suggestions = search_svc.export_manual_suggestions().execute_query()
    if suggestions and suggestions.value:
        suggested_queries = suggestions.value.properties.get("suggestedQueries", [])
        print(f"Manual query suggestions ({len(suggested_queries)}):")
        for sq in suggested_queries[:5]:
            print(f"  - {sq}")
    else:
        print("(No manual suggestions configured)")
    print()

    # -- Step 4: document crawl log diagnostics --
    try:
        crawl_log = DocumentCrawlLog.create(ctx)
        print("Document crawl log:")
        # Get crawled URLs (first page)
        urls = crawl_log.get_crawled_urls().execute_query()
        if urls and urls.value:
            data = urls.value
            if hasattr(data, "rows") and data.rows:
                print(f"  Crawl log entries: {len(data.rows)}")
                for row in data.rows[:5]:
                    print(f"    URL: {row[0] if len(row) > 0 else '?'}")
            else:
                print(f"  Crawl log entries: {len(urls.value)}")
        else:
            print("  (no crawl log data)")

        # Get unsuccessful crawls
        failed = crawl_log.get_unsuccesful_crawled_urls().execute_query()
        if failed and failed.value:
            data = failed.value
            if hasattr(data, "rows") and data.rows:
                print(f"  Unsuccessful URLs: {len(data.rows)}")
                for row in data.rows[:5]:
                    print(f"    URL: {row[0] if len(row) > 0 else '?'}  error: {row[1] if len(row) > 1 else '?'}")
    except Exception as e:
        print(f"  (crawl diagnostics not available: {e})")


if __name__ == "__main__":
    main()
