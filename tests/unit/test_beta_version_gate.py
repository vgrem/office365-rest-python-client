"""A preview-only type is a member of the one tree, but not of every service root.

The model is one tree on purpose: the version picks the root a request is addressed to,
not the surface the model offers. That leaves exactly one hole -- a stable client can hold
a class only the preview root declares, and the request it would build names a path the
stable root has no entity for. The gate closes that hole at the two places the tree is
entered: constructing the object, and naming the collection item type.
"""

import pytest
from office365.common.mail_folder_operation import MailFolderOperation
from office365.common.mention import Mention
from office365.entity import Entity
from office365.graph_client import GraphClient
from office365.graph_version import GraphVersion
from office365.outlook.mail.messages.message import Message
from office365.runtime.types.odata_property import NotSupportedInVersion, odata, version

TENANT = "contoso.onmicrosoft.com"


def _stable() -> GraphClient:
    return GraphClient(tenant=TENANT)


def _beta() -> GraphClient:
    return GraphClient(tenant=TENANT, version=GraphVersion.BETA)


def test_the_declaration_reaches_the_class():
    """One decorator, one storage: the gate is the class attribute it sets, nothing mirrored."""
    assert Mention._versions == frozenset({"beta"})


def test_the_decorator_declares_whatever_roots_it_names():
    """The runtime stores the declaration; it does not read Graph's enum to make sense of it."""

    @version("beta", "v1.0")
    class Probe(Entity):
        pass

    assert Probe._versions == frozenset({"beta", "v1.0"})


def test_a_declaration_naming_no_root_is_not_writable():
    """``@version()`` would say nothing while looking like a rule, so it does not exist."""
    with pytest.raises(TypeError):
        version()


def test_a_type_both_roots_declare_carries_no_gate():
    """``Message`` is v1.0's; only some of its members are the preview root's."""
    assert Message._versions == ()


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
    """One member only the preview root declares -- the shape SharePoint also uses."""

    @odata(name="preview", beta=True)
    @property
    def preview(self):
        return self.properties.get("preview", None)


def test_a_client_that_states_no_version_is_not_gated_by_one():
    """A marker in a tree whose service has no second root is provenance, not a switch."""
    assert _PreviewMember._schema.wire_name("preview", None) == "preview"
    with pytest.raises(NotSupportedInVersion):
        _PreviewMember._schema.wire_name("preview", GraphVersion.V1.value)
