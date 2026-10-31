"""Test-suite helpers.

Configuration lives in :mod:`tests.settings` as one :class:`~tests.settings.Settings`
object. The ``test_*`` names below are the suite's older spelling of the same values;
they are resolved from the object rather than restated, so a field added to
:class:`Settings` is available under both names at once.
"""

import random
import string

from office365.runtime.auth.client_credential import ClientCredential
from office365.runtime.auth.user_credential import UserCredential

from tests.settings import Settings
from tests.settings import settings as _settings

#: ``test_<name>`` names the settings field is not spelled like.
_RENAMED = {
    "test_admin_principal_name": "admin_username",
    "test_tenant_name": "tenant_prefix",
    "test_user_principal_name": "user_principal",
    "test_user_principal_name_alt": "user_principal_alt",
}


def __getattr__(name: str):
    field = _RENAMED.get(name, name.removeprefix("test_"))
    if field in Settings.__dataclass_fields__:
        return getattr(_settings, field)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


# Credential containers are only built when their inputs are configured, so
# importing ``tests`` never fails on a machine without a ``.env``. Live tests
# that use them are skipped by ``tests/conftest.py`` when credentials are absent.
test_client_credentials = (
    ClientCredential(_settings.client_id, _settings.client_secret) if _settings.client_secret else None
)
test_user_credentials = (
    UserCredential(_settings.username, _settings.password) if _settings.username and _settings.password else None
)
test_admin_credentials = test_user_credentials


def create_unique_name(prefix: str) -> str:
    return prefix + "".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))


def create_unique_file_name(prefix: str, ext: str) -> str:
    return create_unique_name(prefix) + "." + ext


def answered_null(result) -> bool:
    """True when the service answered a ``null`` payload for a ``ClientResult``.

    ``ClientResult.value`` asserts that something was read, so a live test that
    checks the *absence* of a value has to ask the result, not the value. The empty
    form is what ``ClientResult.__str__`` prints; this is the one place that knows
    the spelling.
    """
    return str(result) == "ClientResult(<empty>)"
