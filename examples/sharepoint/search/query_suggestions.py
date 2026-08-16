"""
Query suggestions and auto-completion for typeahead search UX.

https://learn.microsoft.com/en-us/sharepoint/dev/general-development/sharepoint-search-rest-api-overview
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import cert_path, cert_thumbprint, client_id, site_url, tenant


def main():
    parser = argparse.ArgumentParser(description="Get search suggestions and auto-completions")
    parser.add_argument("query", help="Query prefix, e.g. 'share'")
    args = parser.parse_args()

    ctx = ClientContext(site_url).with_client_certificate(
        tenant, client_id=client_id, thumbprint=cert_thumbprint, cert_path=cert_path
    )

    # 1. Query suggestions (did-you-mean style)
    suggestions = ctx.search.suggest(args.query).execute_query().value
    print("Query suggestions:")
    for q in suggestions.Queries:
        print(f"  {q.Query}")
    if len(suggestions.PeopleNames):
        print("People:")
        for name in suggestions.PeopleNames:
            print(f"  {name}")

    # 2. Auto-completions (typeahead)
    completions = ctx.search.auto_completions(args.query, number_of_completions=10).execute_query().value
    print("\nAuto-completions:")
    for c in completions.Queries:
        print(f"  {c.Query}")


if __name__ == "__main__":
    main()
