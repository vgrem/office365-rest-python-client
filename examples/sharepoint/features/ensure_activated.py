"""Demonstrates how to ensure a site feature is activated.

Official documentation: https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/csom/features
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.features.definitions.scope import FeatureDefinitionScope
from office365.sharepoint.features.known_list import KnownFeaturesList
from tests.settings import client_id, client_secret, site_url, tenant


def main():
    parser = argparse.ArgumentParser(description="Ensure a site feature is activated")
    parser.add_argument("--site-url", default=site_url, help="target site URL")
    args = parser.parse_args()

    ctx = ClientContext(args.site_url).with_client_secret(tenant, client_id, client_secret)
    feature = ctx.site.features.add(
        KnownFeaturesList.ContentTypeHub, False, FeatureDefinitionScope.Farm, True
    ).execute_query()
    print(f"Feature {feature.display_name} has been activated.")


if __name__ == "__main__":
    main()
