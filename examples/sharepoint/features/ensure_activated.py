"""Demonstrates how to ensure a site feature is activated.

Official documentation: https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/csom/features
"""

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.features.definitions.scope import FeatureDefinitionScope
from office365.sharepoint.features.known_list import KnownFeaturesList
from tests import test_client_credentials, test_site_url

ctx = ClientContext(test_site_url).with_credentials(test_client_credentials)
feature = ctx.site.features.add(
    KnownFeaturesList.ContentTypeHub, False, FeatureDefinitionScope.Farm, True
).execute_query()
print(f"Feature {feature.display_name} has been activated.")
