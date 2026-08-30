"""
Gets information about the term store.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/taxonomy
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import cert_path, cert_thumbprint, client_id, site_url, tenant


def main():
    argparse.ArgumentParser(description="Get term store information").parse_args()

    ctx = ClientContext(site_url).with_client_certificate(
        tenant, client_id=client_id, thumbprint=cert_thumbprint, cert_path=cert_path
    )
    term_store = ctx.taxonomy.term_store.get().execute_query()
    print(term_store)


if __name__ == "__main__":
    main()
