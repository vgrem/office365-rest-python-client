"""A preview-only type is a member of the one tree, but not of every service root.

The model is one tree on purpose: the version picks the root a request is addressed to,
not the surface the model offers. That leaves one hole -- a stable client can hold a class,
or a member, only the preview root declares, and the request it would build names a path or
a key the stable root has no schema for. The gate closes it wherever the tree is *named*:
constructing the object, naming the collection item type, selecting or sending a member,
calling an operation -- and, for a caller asking rather than sending, ``dir()``/``hasattr``:
a member this client's root does not declare is absent from it, not merely refused later.
"""

import pytest
from office365.common.mail_folder_operation import MailFolderOperation
from office365.common.mention import Mention
from office365.entity import Entity
from office365.graph_client import GraphClient
from office365.graph_version import GraphVersion
from office365.outlook.mail.messages.message import Message
from office365.runtime.client_result import ClientResult
from office365.runtime.queries.function import FunctionQuery
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.runtime.types.odata_property import NotSupportedInVersion, odata
from typing_extensions import Self

TENANT = "contoso.onmicrosoft.com"


def _stable() -> GraphClient:
    return GraphClient(tenant=TENANT)


def _beta() -> GraphClient:
    return GraphClient(tenant=TENANT, version=GraphVersion.BETA)


def test_a_type_both_roots_declare_carries_no_gate():
    """``Message`` is v1.0's; only some of its members are the preview root's."""
    assert Message._schema.versions == frozenset()


def test_a_stable_client_refuses_to_build_a_preview_only_type():
    with pytest.raises(NotSupportedInVersion) as raised:
        Mention(_stable())

    assert "Mention" in str(raised.value)
    assert "v1.0" in str(raised.value)


def test_a_beta_client_builds_the_same_class():
    assert Mention(_beta()).properties is not None
    assert MailFolderOperation(_beta()) is not None


def test_a_stable_client_cannot_reach_a_preview_only_collection():
    """The item type is named before a page is asked for, so the refusal lands here."""
    with pytest.raises(NotSupportedInVersion):
        _ = Message(_stable()).mentions


def test_a_beta_client_reaches_the_same_collection():
    assert Message(_beta()).mentions.resource_path is not None


def test_a_type_with_no_gate_is_never_refused():
    """Absence of a gate means "every root", which is what a hand-written class says."""
    assert Message(_stable()) is not None


class _PreviewMember(Entity):
    """One member only each root declares -- the shape SharePoint also uses."""

    @odata(name="preview", beta=True)
    @property
    def preview(self):
        return self.properties.get("preview", None)

    @odata(name="retired", beta=False)
    @property
    def retired(self):
        return self.properties.get("retired", None)

    @odata(name="rename", beta="renamed")
    @property
    def renamed(self):
        return self.properties.get("rename", None)


def test_a_client_that_states_no_version_is_not_gated_by_one():
    """A marker in a tree whose service has no second root is provenance, not a switch."""
    assert _PreviewMember._schema.wire_name("preview", None) == "preview"
    with pytest.raises(NotSupportedInVersion):
        _PreviewMember._schema.wire_name("preview", GraphVersion.V1.value)


def test_a_member_one_root_does_not_declare_is_not_on_that_client():
    """Holding it is not the error; naming it is -- and a name that is not there is absent."""
    stable = _PreviewMember(_stable())
    assert "preview" not in dir(stable)
    assert not hasattr(stable, "preview")
    with pytest.raises(NotSupportedInVersion):
        _ = stable.preview
    assert stable.get_property("preview", "absent") == "absent"


def test_the_same_member_is_on_the_root_that_declares_it():
    beta = _PreviewMember(_beta())
    assert "preview" in dir(beta)
    assert beta.preview is None


def test_the_absence_is_symmetric():
    """A member the preview root dropped is absent from a beta client, by the same rule."""
    assert not hasattr(_PreviewMember(_beta()), "retired")
    assert _PreviewMember(_stable()).retired is None
    assert "retired" not in dir(_PreviewMember(_beta()))


def test_a_member_both_roots_declare_is_never_gated():
    """Under another name it is still declared by both, so both clients answer for it."""
    assert _PreviewMember(_stable()).renamed is None
    assert _PreviewMember(_beta()).renamed is None
    assert "renamed" in dir(_PreviewMember(_stable()))


def test_a_preview_operation_cannot_even_be_named_by_a_stable_client():
    """A method that gated only *when called* would still answer ``hasattr``."""
    stable = _PreviewOperations(_stable())
    assert "preview_action" not in dir(stable)
    assert not hasattr(stable, "preview_action")
    assert hasattr(stable, "stable_action")


def test_a_model_of_the_unversioned_service_keeps_a_marker_as_provenance():
    """A SharePoint page on the offline Graph stand-in must not inherit its version.

    ``SitePage`` carries preview markers from its own document, and the offline helper is
    a ``GraphClient`` because a model object cannot exist without a context. Reading the
    page must not be refused for a version the page's service never stated -- which is
    what the OData type name decides: ``SP.Publishing.SitePage``, not ``microsoft.graph.*``.
    """
    from office365.migration.offline import offline_context
    from office365.sharepoint.publishing.pages.page import SitePage

    page = SitePage(offline_context()).hydrate({"CanvasContent1": "<div/>"})
    assert "canvas_content" in dir(page)
    assert page.canvas_content == "<div/>"


class _PreviewOperations(Entity):
    """Two operations only the preview root declares -- one of each query kind.

    An operation has no payload key a root could refuse: its name *is* the URL, and the
    query is the first place that name exists. So the gate sits there, and both query
    kinds are here because they reach it by different constructors.
    """

    @odata(name="previewAction", beta=True, selectable=False)
    def preview_action(self) -> Self:
        query = ServiceOperationQuery(self, "previewAction", None, {}, None, None)
        self.context.add_query(query)
        return self

    @odata(name="previewFunction", beta=True, selectable=False)
    def preview_function(self) -> ClientResult[bool]:
        return FunctionQuery(self, "previewFunction", None, bool)

    def stable_action(self) -> Self:
        query = ServiceOperationQuery(self, "stableAction", None, {}, None, None)
        self.context.add_query(query)
        return self


def test_a_stable_client_refuses_a_preview_only_operation():
    preview = _PreviewOperations(_stable())
    with pytest.raises(NotSupportedInVersion) as raised:
        preview.preview_action()

    assert "previewAction" in str(raised.value)
    assert "v1.0" in str(raised.value)

    with pytest.raises(NotSupportedInVersion):
        preview.preview_function()


def test_a_beta_client_calls_the_same_operations():
    preview = _PreviewOperations(_beta())
    assert preview.preview_action() is preview
    assert preview.preview_function() is not None


def test_an_operation_no_marker_declares_is_not_gated():
    """The snapshots never disagreed about it, so no root has anything to refuse."""
    assert _PreviewOperations(_stable()).stable_action() is not None


def test_an_operation_is_not_a_column():
    """``selectable=False``: the type has the member, its resource has no such property."""
    assert "previewAction" not in _PreviewOperations._schema.columns
    assert "previewFunction" not in _PreviewOperations._schema.columns
