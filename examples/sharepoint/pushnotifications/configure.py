"""
Configure and use push notifications in SharePoint apps.

https://learn.microsoft.com/en-us/sharepoint/dev/sp-add-ins/push-notifications-in-sharepoint
"""

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.features.definitions.scope import FeatureDefinitionScope
from office365.sharepoint.features.known_list import KnownFeaturesList
from tests import test_client_credentials, test_site_url


def subscribe_to_service():
    """"""


ctx = ClientContext(test_site_url).with_credentials(test_client_credentials)
f = ctx.web.features.add(KnownFeaturesList.PushNotifications, False, FeatureDefinitionScope.Farm, True).execute_query()
print("Feature has been activated.")
