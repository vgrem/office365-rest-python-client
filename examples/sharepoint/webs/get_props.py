"""
Retrieve only selected properties (Author) of a website.

The client library queries only for those properties on the server via select and expand methods,
and the server sends only those properties to the client.
This technique reduces unnecessary data transfer between the client and the server.

See https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/site-operations
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import cert_path, cert_thumbprint, client_id, site_url, tenant


def main():
    parser = argparse.ArgumentParser(description="Retrieve selected properties (Author) of a web")
    parser.add_argument("--site-url", default=site_url, help="target site URL")
    args = parser.parse_args()

    client = ClientContext(args.site_url).with_client_certificate(
        tenant, client_id=client_id, thumbprint=cert_thumbprint, cert_path=cert_path
    )
    web = client.web.get().expand(["Author"]).execute_query()
    print(web.author)


if __name__ == "__main__":
    main()
