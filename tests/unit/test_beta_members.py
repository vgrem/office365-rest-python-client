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
from office365.outlook.calendar.events.event import Event
from office365.outlook.contacts.contact import Contact
from office365.runtime.client_object import ClientObject
from office365.runtime.odata.v4.json_format import V4JsonFormat
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.queries.read_entity import ReadEntityQuery
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


def test_select_all_is_narrowed_to_what_the_root_can_honour():
    """``select_all()`` is one class-level list; the URL carries what the root has."""
    assert AccessPackage.select_all() == [
        "id",
        "catalogId",
        "createdBy",
        "isRoleScopesVisible",
        "modifiedBy",
        "uniqueName",
    ]

    stable = AccessPackage(_client(), ResourcePath("accessPackages"))
    preview = AccessPackage(_client(GraphVersion.BETA), ResourcePath("accessPackages"))
    stable.query_options.select = list(AccessPackage.select_all())
    preview.query_options.select = list(AccessPackage.select_all())

    assert ReadEntityQuery(stable).url.endswith("?$select=id")
    assert ReadEntityQuery(preview).url.endswith(
        "?$select=id,catalogId,createdBy,isRoleScopesVisible,modifiedBy,uniqueName"
    )


def test_the_narrowing_does_not_rewrite_the_projection_the_caller_built():
    """The gate answers for one request; the object keeps the list it was given."""
    stable = AccessPackage(_client(), ResourcePath("accessPackages"))
    stable.query_options.select = list(AccessPackage.select_all())

    url = ReadEntityQuery(stable).url

    assert url.endswith("?$select=id")
    assert stable.query_options.select == list(AccessPackage.select_all())


def test_a_preview_only_member_never_reaches_a_stable_select():
    """The pilot's exit test: an Event export written before beta selects the same names.

    ``Event.select_all()`` grew by the two members beta declares, which is additive and
    harmless. What must not happen is a stable request asking for them: Microsoft Graph
    rejects a ``$select`` it cannot honour, so a marker that leaked into the projection
    would break every existing calendar export rather than add a column.
    """
    columns = Event.select_all()
    assert columns[-2:] == ["occurrenceId", "uid"]

    stable = Event(_client(), ResourcePath("events"))
    preview = Event(_client(GraphVersion.BETA), ResourcePath("events"))
    stable.query_options.select = list(columns)
    preview.query_options.select = list(columns)

    assert ReadEntityQuery(stable).url.endswith("?$select=" + ",".join(columns[:-2]))
    assert ReadEntityQuery(preview).url.endswith("?$select=" + ",".join(columns))


def test_the_contact_columns_a_stable_client_selects_are_the_ones_it_always_selected():
    """The other direction of the pilot: 7 members the preview root dropped.

    ``select_all()`` still lists them because the model declares them -- the stable root
    answers them and a v1.0 export must keep asking. What changes is the preview
    projection, where they are gone: beta replaced the three phone fields with
    ``phones``, so a beta ``$select`` asking for ``businessPhones`` would be rejected.
    """
    schema = Contact._schema
    columns = list(Contact.select_all())

    assert schema.stable_only == {
        "businessAddress",
        "businessHomePage",
        "businessPhones",
        "homeAddress",
        "homePhones",
        "mobilePhone",
        "otherAddress",
    }
    assert schema.projection(columns, "v1.0") == columns
    assert schema.projection(columns, PREVIEW) == [name for name in columns if name not in schema.stable_only]
    assert len(columns) == len(schema.projection(columns, PREVIEW)) + 7
