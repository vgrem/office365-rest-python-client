"""Demonstrates how to save a list as a template in the list template gallery

Official documentation: https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/list-operations
"""

from office365.sharepoint.client_context import ClientContext
from tests import test_client_credentials, test_team_site_url

ctx = ClientContext(test_team_site_url).with_credentials(test_client_credentials)
ctx.web.lists.get_by_title("Site Pages").save_as_template("SitePages.stp", "Site Pages", "", True).execute_query()
