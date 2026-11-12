"""What a method is, when it is a command: one stamp, one reader.

The four generic commands are declared once, on the base class that provides them, so
every type in the library answers them without a line of its own. What is asserted here
is that the reader agrees with the library's own hierarchy: a collection lists and
creates, an entity gets, updates and deletes, and a method that declares nothing is not
a command rather than a command with no name.
"""

import pytest
from office365.capabilities import capabilities_of
from office365.directory.users.user import User
from office365.outlook.mail.messages.collection import MessageCollection
from office365.outlook.mail.messages.message import Message
from office365.runtime.verbs import EFFECTS, ROLES, VerbMeta, declared_verb, verb
from office365.sharepoint.lists.list import List


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
