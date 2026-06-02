"""Demonstrates how to deactivate a site feature.

Official documentation: https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/csom/features
"""

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.features.definitions.scope import FeatureDefinitionScope
from office365.sharepoint.features.known_list import KnownFeaturesList
from tests import test_client_credentials, test_site_url

ctx = ClientContext(test_site_url).with_credentials(test_client_credentials)

# Activate a feature first, then deactivate it
f = ctx.site.features.add(KnownFeaturesList.ContentTypeHub, False, FeatureDefinitionScope.Farm).execute_query()
print(f"Activated: {f.display_name}")

# Deactivate (remove) the feature
f.delete_object().execute_query()
print(f"Deactivated: {f.display_name}")
