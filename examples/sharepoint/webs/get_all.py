"""Subsite inventory report.

Enumerates all webs (root + subsites) in the site collection and prints each
web's template, created date and language, plus a summary grouped by template.

See https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/site-operations
"""

import argparse
from collections import Counter

from office365.runtime.operations import Progress
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.webs.web import Web
from tests.settings import cert_path, cert_thumbprint, client_id, site_url, tenant


def progress_bar(description: str):
    """tqdm-backed hook — the library only needs a ``Callable[[Progress], None]``."""
    from tqdm import tqdm

    bar = tqdm(desc=description)

    def hook(p: Progress[Web]) -> None:
        bar.update(p.done - bar.n)

    return hook


def main():
    parser = argparse.ArgumentParser(description="Subsite inventory report")
    parser.add_argument("--site-url", default=site_url, help="target site collection URL")
    parser.add_argument("--no-progress", action="store_true", help="do not show a tqdm progress bar")
    args = parser.parse_args()

    client = ClientContext(args.site_url).with_client_certificate(
        tenant, client_id=client_id, thumbprint=cert_thumbprint, cert_path=cert_path
    )

    hook = None if args.no_progress else progress_bar("Scanning webs")
    webs = client.web.get_all_webs(progress=hook).execute_query()
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
