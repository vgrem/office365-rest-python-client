from office365.sharepoint.client_context import ClientContext
from tests import test_client_credentials, test_team_site_url

ctx = ClientContext(test_team_site_url).with_credentials(test_client_credentials)
lib = ctx.web.lists.get_by_title("Documents")
items = lib.items
ctx.load(items, ["EncodedAbsUrl"])
ctx.execute_query()
for item in items:
    print("{0}".format(item.properties.get("EncodedAbsUrl")))
