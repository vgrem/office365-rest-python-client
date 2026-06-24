"""
Search-as-you-type suggestions: query keywords, people names, and popular results.

Uses the SharePoint Search suggest API to power autocomplete/search-as-you-type
scenarios — the same API PnP Modern Search calls for its suggestion provider.

https://learn.microsoft.com/en-us/sharepoint/dev/general-development/sharepoint-search-rest-api-overview
"""

from office365.sharepoint.client_context import ClientContext
from tests import test_client_id, test_password, test_site_url, test_tenant, test_username

ctx = ClientContext(test_site_url).with_username_and_password(
    tenant=test_tenant,
    client_id=test_client_id,
    username=test_username,
    password=test_password,
)

# Partial query — as a user types "guide" the suggest API returns completions
result = ctx.search.suggest("guide").execute_query()
suggestions = result.value

print("=== Query Suggestions ===")
for q in suggestions.Queries:
    source = "personal" if q.IsPersonal else "global"
    print(f"  [{source}] {q.Query}")

print("\n=== People Name Suggestions ===")
for name in suggestions.PeopleNames:
    print(f"  {name}")

print("\n=== Popular Results ===")
for item in suggestions.PopularResults:
    print(f"  {item.Title} — {item.Url}")
