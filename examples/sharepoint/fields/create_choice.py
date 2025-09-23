"""
Demonstrates how to create lookup field
"""

from office365.sharepoint.client_context import ClientContext
from tests import (
    create_unique_name,
    test_client_id,
    test_client_secret,
    test_team_site_url,
)

client = ClientContext(test_team_site_url).with_client_credentials(
    test_client_id, test_client_secret
)
lib = client.web.default_document_library()

field_name = create_unique_name("ChoiceField")

choices = ["Not Started", "In Progress", "Completed", "Deferred"]
field = lib.fields.add_choice_field(title=field_name, values=choices).execute_query()

field.delete_object().execute_query()  # clean up
