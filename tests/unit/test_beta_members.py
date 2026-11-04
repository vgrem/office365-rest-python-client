"""One model tree, two service roots: a client's version decides what it can name.

The declaration carries the difference -- ``beta=True`` for a member only the preview
root declares, ``beta="otherName"`` for one it renames, ``beta=False`` for one it
dropped -- and everything else is derived from it: the payload key, the navigation
path segment, the ``$select`` a projection carries, and the error a stable client gets
for naming something the stable schema has no room for.
"""

import pytest
from office365.directory.identitygovernance.entitlementmanagement.accesspackage.package import AccessPackage
from office365.graph_client import GraphClient
from office365.graph_version import GraphVersion
from office365.runtime.client_object import ClientObject
from office365.runtime.odata.v4.json_format import V4JsonFormat
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.queries.read_entity import ReadEntityQuery
from office365.runtime.schema import TypeSchema
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


def test_a_projection_keeps_the_names_the_root_declares_and_spells_them_its_way():
    """$select and $expand are bulk, so they are narrowed rather than refused."""
    schema = AccessPackage._schema

    assert schema.projection(["id", "uniqueName"], "v1.0") == ["id"]
    assert schema.projection(["id", "uniqueName"], PREVIEW) == ["id", "uniqueName"]
    # No version at all is SharePoint: nothing here has an opinion, so nothing moves.
    assert schema.projection(["id", "uniqueName"], None) == ["id", "uniqueName"]
    # A name the model never declared is not this gate's business.
    assert schema.projection(["dataSource"], "v1.0") == ["dataSource"]
    # An expanded navigation is spelled the way the request's root spells it.
    assert schema.projection(["catalog"], PREVIEW) == ["accessPackageCatalog"]


def test_columns_is_narrowed_to_what_the_root_can_honour():
    """``TypeSchema.columns`` is one class-level list; the URL carries what the root has."""
    columns = list(TypeSchema.of(AccessPackage).columns)
    beta_only = AccessPackage._schema.beta_only
    stable_columns = [name for name in columns if name not in beta_only]
    # The class declares more than the preview subset -- the members its getters spell --
    # so the narrowing is exercised by the difference, not by a frozen pair of lists.
    assert set(beta_only) < set(columns)

    stable = AccessPackage(_client(), ResourcePath("accessPackages"))
    preview = AccessPackage(_client(GraphVersion.BETA), ResourcePath("accessPackages"))
    stable.query_options.select = list(columns)
    preview.query_options.select = list(columns)

    assert ReadEntityQuery(stable).url.endswith("?$select=" + ",".join(stable_columns))
    assert ReadEntityQuery(preview).url.endswith("?$select=" + ",".join(columns))
    assert "uniqueName" in columns
    assert "uniqueName" not in stable_columns


def test_the_narrowing_does_not_rewrite_the_projection_the_caller_built():
    """The gate answers for one request; the object keeps the list it was given."""
    stable = AccessPackage(_client(), ResourcePath("accessPackages"))
    stable.query_options.select = list(TypeSchema.of(AccessPackage).columns)

    url = ReadEntityQuery(stable).url

    assert "uniqueName" not in url
    assert stable.query_options.select == list(TypeSchema.of(AccessPackage).columns)
