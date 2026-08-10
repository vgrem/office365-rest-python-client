"""Site metadata summary.

Prints the site's basic metadata: library version and full URLs from the
context web information, plus web properties (title, template, language,
created date).

See https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/site-operations
"""

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.webs.web import Web
from tests import test_client_credentials, test_site_url

ctx = ClientContext(test_site_url).with_credentials(test_client_credentials)

info = Web.get_context_web_information(ctx).execute_query()
web = ctx.web.get().execute_query()

print(f"Library version: {info.value.LibraryVersion}")
print(f"Site URL: {info.value.SiteFullUrl}")
print(f"Web URL: {info.value.WebFullUrl}")
print(f"Title: {web.title}")
print(f"Template: {web.web_template}   language: {web.language}   created: {web.created:%Y-%m-%d}")
