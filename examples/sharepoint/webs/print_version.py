"""Site metadata summary.

Prints the site's basic metadata: library version and full URLs from the
context web information, plus web properties (title, template, language,
created date).

See https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/site-operations
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.webs.web import Web
from tests.settings import cert_path, cert_thumbprint, client_id, site_url, tenant


def main():
    parser = argparse.ArgumentParser(description="Print site metadata summary")
    parser.add_argument("--site-url", default=site_url, help="target site URL")
    args = parser.parse_args()

    ctx = ClientContext(args.site_url).with_client_certificate(
        tenant, client_id=client_id, thumbprint=cert_thumbprint, cert_path=cert_path
    )

    info = Web.get_context_web_information(ctx).execute_query()
    web = ctx.web.get().execute_query()

    print(f"Library version: {info.value.LibraryVersion}")
    print(f"Site URL: {info.value.SiteFullUrl}")
    print(f"Web URL: {info.value.WebFullUrl}")
    print(f"Title: {web.title}")
    print(f"Template: {web.web_template}   language: {web.language}   created: {web.created:%Y-%m-%d}")


if __name__ == "__main__":
    main()
