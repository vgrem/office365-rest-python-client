"""Subsite inventory report.

Enumerates all webs (root + subsites) in the site collection and prints each
web's template, created date and language, plus a summary grouped by template.

See https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/site-operations
"""

import argparse
from collections import Counter

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, client_secret, site_url, tenant


def main():
    parser = argparse.ArgumentParser(description="Subsite inventory report")
    parser.add_argument("--site-url", default=site_url, help="target site collection URL")
    args = parser.parse_args()

    client = ClientContext(args.site_url).with_client_secret(tenant, client_id, client_secret)

    webs = client.web.get_all_webs().get().execute_query()
    print(f"Webs ({len(webs)}):")
    for web in sorted(webs, key=lambda w: w.url or ""):
        print(
            f"  {web.url:55s} template={web.web_template or '?':15s} created={web.created:%Y-%m-%d}"
            f" lang={web.language or '?'}"
        )

    by_template = Counter(web.web_template or "?" for web in webs)
    print("\nSummary by template:")
    for template, count in by_template.most_common():
        print(f"  {template:15s} {count}")


if __name__ == "__main__":
    main()
