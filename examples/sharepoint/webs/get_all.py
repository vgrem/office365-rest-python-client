"""Subsite inventory report.

Enumerates all webs (root + subsites) in the site collection and prints each
web's template, created date and language, plus a summary grouped by template.

See https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/site-operations
"""

from collections import Counter

from office365.sharepoint.client_context import ClientContext
from tests import test_client_credentials, test_site_url


def main():
    client = ClientContext(test_site_url).with_credentials(test_client_credentials)

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
