"""Gets trending hash tags (up to 20 most popular over the past week).

https://learn.microsoft.com/en-us/sharepoint/dev/apis/people-rest-api
"""

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.userprofiles.people_manager import PeopleManager
from tests import test_client_id, test_password, test_site_url, test_tenant, test_username

ctx = ClientContext(test_site_url).with_username_and_password(
    tenant=test_tenant,
    client_id=test_client_id,
    username=test_username,
    password=test_password,
)
tags = PeopleManager.get_trending_tags(ctx).execute_query()
for tag in tags.items:
    print(f"  #{tag.name}  ({tag.count})")
