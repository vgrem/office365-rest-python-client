"""What a caller is told before running a command: the join, not a copy.

Every line `hints_of` answers with is a fact some declaration already states. These tests
pin that each fact reaches the caller for the command that has it and stays quiet for the
command that does not, which is the whole claim: a help page prints what the model said.
"""

import pytest
from office365.capabilities import capabilities_of, hints_of
from office365.directory.users.user import User
from office365.intune.devices.compliance.script_device_state import DeviceComplianceScriptDeviceState
from office365.intune.devices.management.managed.device import ManagedDevice
from office365.outlook.mail.messages.message import Message
from office365.runtime.client_object_collection import ClientObjectCollection


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
