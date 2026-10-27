"""One model tree, two service roots: a client's version decides what it can name.

The declaration carries the difference -- ``beta=`` for a member the preview root
renames, ``since=`` for one only it declares -- and everything else is derived from
it: the payload key, the navigation path segment, and the error a stable client gets
for naming something the stable schema has no room for.
"""

import pytest
from office365.directory.identitygovernance.entitlementmanagement.accesspackage.package import AccessPackage
from office365.graph_client import GraphClient
from office365.graph_version import GraphVersion
from office365.runtime.client_object import ClientObject
from office365.runtime.odata.v4.json_format import V4JsonFormat
from office365.runtime.types.odata_property import PREVIEW, NotSupportedInVersion, odata

TENANT = "contoso.onmicrosoft.com"


class _Dropped(ClientObject):
    """A member the preview root no longer declares: ``groupSetting`` is one of 29 types."""

    @odata(name="legacyOnly", beta=False)
    @property
    def legacy_only(self):
        return self.properties.get("legacyOnly", None)


def _client(version=None):
    return GraphClient(tenant=TENANT) if version is None else GraphClient(tenant=TENANT, version=version)


def _url(obj):
    path = obj.resource_path
    assert path is not None
    return path.to_url()


def _payload(package):
    return package.to_json(V4JsonFormat("none"))


def test_the_preview_token_is_the_beta_service_root():
    """The runtime never imports the service enum; this is the one string they share."""
    assert PREVIEW == GraphVersion.BETA.value


def test_the_declaration_is_the_only_place_the_two_names_appear():
    schema = AccessPackage._schema

    assert schema.beta_names == {
        "assignmentPolicies": "accessPackageAssignmentPolicies",
        "catalog": "accessPackageCatalog",
        "resourceRoleScopes": "accessPackageResourceRoleScopes",
    }
    assert schema.canonical_names["accessPackageCatalog"] == "catalog"
    assert schema.beta_only == {"catalogId", "createdBy", "isRoleScopesVisible", "modifiedBy", "uniqueName"}


def test_a_renamed_member_is_sent_under_the_name_the_client_declares():
    stable = AccessPackage(_client()).set_property("catalog", "cat-123")
    preview = AccessPackage(_client(GraphVersion.BETA)).set_property("catalog", "cat-123")

    assert _payload(stable) == {"catalog": "cat-123"}
    assert _payload(preview) == {"accessPackageCatalog": "cat-123"}


def test_a_preview_only_member_cannot_be_sent_by_a_stable_client():
    payload = AccessPackage(_client(GraphVersion.BETA)).set_property("uniqueName", "contoso")
    assert _payload(payload) == {"uniqueName": "contoso"}

    stable = AccessPackage(_client()).set_property("uniqueName", "contoso")
    with pytest.raises(NotSupportedInVersion) as raised:
        _payload(stable)

    assert raised.value.member == "uniqueName"
    assert raised.value.declared_by == PREVIEW


def test_a_preview_response_is_read_under_the_model_name():
    """The preview root spells a renamed member its own way; the model holds one name."""
    package = AccessPackage(_client(GraphVersion.BETA)).hydrate({"id": "1", "accessPackageCatalog": {"id": "cat-123"}})

    assert package.properties["catalog"].id == "cat-123"
    assert package.catalog.id == "cat-123"
    assert "accessPackageCatalog" not in package.properties


def test_a_navigation_path_follows_the_client_version():
    stable = AccessPackage(_client())
    preview = AccessPackage(_client(GraphVersion.BETA))

    assert _url(stable.catalog) == "/catalog"
    assert _url(preview.catalog) == "/accessPackageCatalog"


def test_a_stable_client_cannot_name_a_preview_only_member_at_all():
    """Not just the payload: any place a member's wire name is derived gates here."""
    with pytest.raises(NotSupportedInVersion):
        AccessPackage(_client()).wire_name("uniqueName")

    assert AccessPackage(_client(GraphVersion.BETA)).wire_name("uniqueName") == "uniqueName"


def test_a_member_only_the_stable_root_declares_cannot_be_sent_to_preview():
    """Beta dropped 86 members; a preview client naming one describes nothing."""
    assert _Dropped._schema.stable_only == {"legacyOnly"}

    preview = _Dropped(_client(GraphVersion.BETA)).set_property("legacyOnly", "x")
    with pytest.raises(NotSupportedInVersion) as raised:
        _payload(preview)

    assert raised.value.member == "legacyOnly"
    assert raised.value.declared_by is None
    assert _payload(_Dropped(_client()).set_property("legacyOnly", "x")) == {"legacyOnly": "x"}


def test_a_member_no_version_disagrees_about_is_named_as_it_always_was():
    """The 3,000 members neither root renames keep the spelling the model held."""
    package = AccessPackage(_client(GraphVersion.BETA)).set_property("displayName", "Contoso")

    assert _payload(package) == {"displayName": "Contoso"}
