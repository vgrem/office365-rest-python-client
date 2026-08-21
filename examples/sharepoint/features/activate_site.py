"""Demonstrates how to activate a site feature.

Official documentation: https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/csom/features
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.features.definitions.scope import FeatureDefinitionScope
from office365.sharepoint.features.known_list import KnownFeaturesList
from tests.settings import client_id, client_secret, team_site_url, tenant


def main():
    parser = argparse.ArgumentParser(description="Activate a site feature")
    parser.add_argument("--site-url", default=team_site_url, help="target site URL")
    args = parser.parse_args()

    ctx = ClientContext(args.site_url).with_client_secret(tenant, client_id, client_secret)
    f = ctx.site.features.add(KnownFeaturesList.DocId, False, FeatureDefinitionScope.Farm).execute_query()
    print(f"Feature {f.display_name} has been activated.")


if __name__ == "__main__":
    main()
