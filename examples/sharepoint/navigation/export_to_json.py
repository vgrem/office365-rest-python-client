"""
Export the whole site navigation — both bars — to a JSON file.

One ``get_tree()`` call reads the navigation, expands both bars so the response
carries them as typed collections, and walks every descendant with a progress
bar. ``to_json()`` then writes that tree as it stands, so each node's ``Children``
come out nested.

A Python port of PnP's ``spo-export-topnavbar-including-translations`` script
sample (without the multilingual title resources).

https://learn.microsoft.com/en-us/sharepoint/dev/apis/navigation-api-reference
"""

import argparse
import json
import tempfile
from pathlib import Path

from office365.runtime.progress import progress_bar
from office365.sharepoint.client_context import ClientContext
from tests.settings import cert_path, cert_thumbprint, client_id, site_url, tenant


def main():
    parser = argparse.ArgumentParser(description="Export the site navigation to JSON")
    parser.add_argument("--site-url", default=site_url, help="site URL")
    parser.add_argument(
        "--output", default=str(Path(tempfile.gettempdir()) / "navigation.json"), help="output JSON file"
    )
    parser.add_argument("--no-progress", action="store_true", help="do not show a tqdm progress bar")
    args = parser.parse_args()

    ctx = ClientContext(args.site_url).with_client_certificate(
        tenant, client_id=client_id, thumbprint=cert_thumbprint, cert_path=cert_path
    )

    hook = None if args.no_progress else progress_bar("Scanning navigation")
    navigation = ctx.web.navigation.get_tree(progress=hook).execute_query()

    tree = navigation.to_json()  # the model's own tree, both bars, children nested
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(tree, f, indent=2)
    print(
        f"Exported {len(navigation.quick_launch)} quick launch and "
        f"{len(navigation.top_navigation_bar)} top nav node(s) to {args.output}"
    )


if __name__ == "__main__":
    main()
