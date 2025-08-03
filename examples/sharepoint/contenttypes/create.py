import logging

from office365.sharepoint.client_context import ClientContext
from tests import test_client_credentials, test_team_site_url

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


ctx = ClientContext(test_team_site_url).with_credentials(test_client_credentials)

logger.info("Creating content type ...")
parent_ct = ctx.web.available_content_types.get_by_name("Document")
ct = ctx.web.content_types.create(
    "Contoso Document", parent_content_type=parent_ct
).execute_query()
# ct = ctx.web.content_types.create("Contoso Document", parent_content_type="0x0101").execute_query()
logger.info(f"Successfully created content type with ID: {ct.id}")

logger.info("Updating content type properties ...")
ct.set_property("Description", "Contoso Document content type").update(
    True
).execute_query()
logger.info("Successfully updated content type properties")

# 3. Link the fields to the content type
# field = ctx.web.fields.get_by_internal_name_or_title("Language")
# ct.field_links.add(field).execute_query()

# 4. Localize content type
logger.info("Adding localization for content type ...")
result = ct.name_resource.set_value_for_ui_culture(
    "fi-FI", "Contoso Dokumentti"
).execute_query()
logger.info("Successfully added localization")


logger.info("Deleting temporary content type ...")
ct.delete_object().execute_query()
logger.info("Cleanup completed successfully")
