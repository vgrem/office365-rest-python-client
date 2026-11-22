"""What a command is, and what a caller is told about it before running one.

A command exists because a method declares itself one: `@verb` states the role, the effect
follows from the role, and the reader in `office365.capabilities` answers from that stamp
rather than from a name. The second half asks what the same declarations print on a help
page -- the permission a command needs, whether it confirms, the licence the type it lives
in carries -- and every line there is a fact some declaration already states. So these two
halves are one subject read in two places: what the model says about a method, and what the
prompt says to the person about to call it.

Silence is the thing both halves refuse. A method that declares nothing is not a command, a
command that names no permission says so rather than saying nothing, and a method that is
not a command is refused rather than described.
"""

from __future__ import annotations

import pytest
from office365.capabilities import capabilities_of, hints_of
from office365.directory.users.user import User
from office365.intune.devices.compliance.script_device_state import DeviceComplianceScriptDeviceState
from office365.intune.devices.management.managed.device import ManagedDevice
from office365.outlook.mail.messages.collection import MessageCollection
from office365.outlook.mail.messages.message import Message
from office365.runtime.client_object_collection import ClientObjectCollection
from office365.runtime.verbs import EFFECTS, ROLES, VerbMeta, declared_verb, paged_of, verb
from office365.sharepoint.lists.list import List

# --- what a method declares about itself ----------------------------------------------


def test_a_collection_lists_and_creates_and_does_not_delete() -> None:
    verbs = capabilities_of(MessageCollection).verbs
    assert {meta.role for meta in verbs.values()} == {"list", "create"}
    assert verbs["get"].name == "list"
    assert verbs["add"].name == "create"


def test_paging_is_a_second_entry_point_for_the_same_command_not_a_second_command() -> None:
    verbs = capabilities_of(MessageCollection).verbs
    assert verbs["get_all"].name == "get-all"
    assert verbs["get_all"].paged is True
    # Declared on purpose and hidden on purpose: the command word is still `list`.
    assert verbs["get_all"].expose is False


def test_the_paged_reader_answers_from_the_declaration_and_nothing_else() -> None:
    paged = paged_of(MessageCollection)
    assert list(paged) == ["get_all"]
    assert paged["get_all"].paged is True
    assert paged["get_all"].expose is False
    # One page, one answer: an entity has no walk-everything form, and neither does a
    # command that simply declares nothing (`paged=None` is not "unknown", it is "no").
    assert paged_of(Message) == {}
    assert paged_of(List) == {}
    # The gathered view answers the same way, so a caller that already holds a type's
    # declared facts does not walk its methods a second time.
    assert capabilities_of(MessageCollection).paged == "get_all"
    assert capabilities_of(Message).paged is None


@pytest.mark.parametrize("entity_type", [Message, List])
def test_an_entity_gets_updates_and_deletes_and_only_the_last_one_confirms(entity_type: type) -> None:
    verbs = capabilities_of(entity_type).verbs
    # A type may declare more than the three it inherits (Message sends, List subscribes),
    # so the claim is that the base trio is there and nothing irreversible is silent about it.
    assert {"get", "update", "delete"} <= {meta.role for meta in verbs.values()}
    assert [name for name, meta in verbs.items() if meta.confirm] == ["delete_object"]
    assert verbs["delete_object"].name == "delete"


def test_a_method_that_declares_nothing_is_not_a_command() -> None:
    # An entity is not a collection: it answers none of the collection's commands.
    verbs = capabilities_of(User).verbs
    assert {"add", "get_all", "paged"} & set(verbs) == set()
    with pytest.raises(ValueError, match="names no verb"):
        declared_verb(User.select)


def test_the_effect_is_inferred_and_only_an_action_has_to_state_it() -> None:
    assert {role: VerbMeta(role=role).effect for role in ROLES if role != "action"} == {
        "list": "read",
        "get": "read",
        "create": "write",
        "update": "write",
        "delete": "destroy",
    }
    with pytest.raises(ValueError, match="states no effect"):
        VerbMeta(role="action")
    assert VerbMeta(role="action", effect="write").effect in EFFECTS
    with pytest.raises(ValueError, match="unknown verb role"):
        VerbMeta(role="upsert")
    # `local` acts on the session and nothing else, which is the one effect a caller can
    # reach with no session yet - so it is the only one that may skip authentication.
    assert not VerbMeta(role="action", effect="local").needs_session
    assert VerbMeta(role="get").needs_session


def test_a_declared_name_wins_and_an_undeclared_one_is_the_method_name() -> None:
    @verb(role="action", effect="write", name="send")
    def send_mail(self: object) -> None: ...

    assert declared_verb(send_mail).name == "send"

    @verb(role="get")
    def get_all(self: object) -> None: ...

    assert declared_verb(get_all).name == "get-all"

    @verb(role="action", effect="local", name="login")
    def with_client_secret(self: object) -> None: ...

    # One command word, six ways to reach it: the method is named after the way it
    # authenticates, so the mode is read off the name unless it is stated.
    assert declared_verb(with_client_secret).name == "login"
    assert declared_verb(with_client_secret).mode == "client-secret"
    assert declared_verb(get_all).mode == ""


# --- what the same declarations print ------------------------------------------------


def test_a_command_reports_the_permission_stamped_on_the_method() -> None:
    permission, *_ = hints_of(User, "delete_object")
    assert "application User.ReadWrite.All" in permission
    assert "delegated User.ReadWrite.All" in permission


def test_a_command_that_destroys_says_it_is_confirmed_and_one_that_sends_does_not() -> None:
    assert any(line.startswith("Confirmed") for line in hints_of(User, "delete_object"))
    assert not any(line.startswith("Confirmed") for line in hints_of(User, "send_mail"))


def test_a_command_that_declares_no_permission_says_so_rather_than_nothing() -> None:
    # Silence would read as "needs nothing", and `Message.delete_object` inherits its
    # request from a base that names no permission -- a debt to see, not to hide.
    assert hints_of(Message, "delete_object")[0] == "Declares no permission."


def test_a_call_answers_the_licence_of_the_type_it_lives_in() -> None:
    # `retire` is stamped with the permission and not with the plan: the plan is the family's,
    # so asking about the call has to reach the class the same way asking about the type does.
    assert capabilities_of(ManagedDevice.retire).licenses == ("INTUNE_A",)


def test_a_preview_only_type_says_only_the_beta_root_answers_it() -> None:
    assert "Only the beta root answers it." in hints_of(DeviceComplianceScriptDeviceState, "delete_object")
    assert "Only the beta root answers it." not in hints_of(User, "delete_object")


def test_a_collection_names_the_form_that_walks_every_page() -> None:
    assert "get_all walks every page." in hints_of(ClientObjectCollection, "get_all")


def test_a_method_that_is_not_a_command_is_refused_rather_than_described() -> None:
    with pytest.raises(ValueError, match="names no verb"):
        hints_of(User, "properties")
