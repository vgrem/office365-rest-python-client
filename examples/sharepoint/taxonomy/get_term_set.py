"""
Finds term sets by name within a term group.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/taxonomy
"""

from office365.sharepoint.client_context import ClientContext
from tests import test_client_credentials, test_team_site_url

ctx = ClientContext(test_team_site_url).with_credentials(test_client_credentials)
term_group = ctx.taxonomy.term_store.term_groups.get_by_name("Geography")
term_sets = term_group.get_term_sets_by_name("Countries").execute_query()
for ts in term_sets:
    print(ts)
