"""
Demonstrates how to perform list/library assessment if taxonomy field value association is broken
to term set or not.

To prevent this exception to occur:
'-2146232832, Microsoft.SharePoint.SPFieldValidationException', 'The given guid does not exist in the term store'
"""

from office365.sharepoint.client_context import ClientContext
from tests import test_client_credentials, test_team_site_url

ctx = ClientContext(test_team_site_url).with_credentials(test_client_credentials)
lib = ctx.web.default_document_library()
result = lib.validate_broken_taxonomy_values().execute_query()
