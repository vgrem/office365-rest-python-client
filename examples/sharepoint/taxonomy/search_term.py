"""
Searches for taxonomy terms by name.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/taxonomy
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import cert_path, cert_thumbprint, client_id, site_url, tenant


def main():
    parser = argparse.ArgumentParser(description="Search for taxonomy terms by name")
    parser.add_argument("--term-name", default="Sweden", help="term name to search for")
    args = parser.parse_args()

    ctx = ClientContext(site_url).with_client_certificate(
        tenant, client_id=client_id, thumbprint=cert_thumbprint, cert_path=cert_path
    )
    terms = ctx.taxonomy.term_store.search_term(args.term_name).execute_query()
    for term in terms:
        print(term.labels[0])


if __name__ == "__main__":
    main()
