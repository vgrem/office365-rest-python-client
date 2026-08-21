"""Demonstrates how to deactivate a site feature.

Official documentation: https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/csom/features
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.features.definitions.scope import FeatureDefinitionScope
from office365.sharepoint.features.known_list import KnownFeaturesList
from tests.settings import client_id, client_secret, site_url, tenant


def main():
    parser = argparse.ArgumentParser(description="Deactivate a site feature")
    parser.add_argument("--site-url", default=site_url, help="target site URL")
    args = parser.parse_args()

    ctx = ClientContext(args.site_url).with_client_secret(tenant, client_id, client_secret)

    # Activate a feature first, then deactivate it
    f = ctx.site.features.add(KnownFeaturesList.ContentTypeHub, False, FeatureDefinitionScope.Farm).execute_query()
    print(f"Activated: {f.display_name}")

    # Deactivate (remove) the feature
    f.delete_object().execute_query()
    print(f"Deactivated: {f.display_name}")


if __name__ == "__main__":
    main()
