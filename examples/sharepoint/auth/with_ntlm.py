"""
Demonstrates how to authenticate with user credentials (username and password) in non-interactive mode
"""

import logging

from office365.sharepoint.client_context import ClientContext
from tests import test_password, test_team_site_url, test_username

logging.basicConfig(level=logging.DEBUG)

ctx = ClientContext(test_team_site_url, allow_ntlm=True).with_user_credentials(
    test_username, test_password
)
web = ctx.web.get().execute_query()
