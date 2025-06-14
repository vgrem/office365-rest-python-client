"""
Create a modern site

"""

import logging
from random import randint

from office365.sharepoint.tenant.administration.tenant import Tenant
from tests import (
    test_admin_site_url,
    test_site_url,
    test_user_credentials,
    test_user_principal_name_alt,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

alias = str(randint(0, 10000))
title = "Custom Site"
site_url = "{0}/sites/{1}".format(test_site_url, alias)

tenant = Tenant.from_url(test_admin_site_url).with_credentials(test_user_credentials)

logger.info(f"Creating a site at: {site_url}")
site = tenant.create_site_sync(site_url, test_user_principal_name_alt).execute_query()

logger.info("\nSite created successfully:")
logger.info(f"  URL: {site.title}")

# Cleanup - delete the test site
# tenant.remove_site(site_url).execute_query()  # cleanup
