"""The last four members the Graph pipeline adds, and the name one type got wrong.

With the declarations back-filled, the generator converges on four types: it finishes
``IdentitySource`` (a value type with no members and no type name), adds ``state`` to
``SearchAnswer`` and the two version bounds to ``DeviceCompliancePolicy`` -- members
every subtype declares, which ``_schema`` therefore answers with ``system=True`` -- and
corrects ``FileStorageContainer``'s type name. Each is pinned here, so the tree stays
converged instead of being regenerated into a diff.
"""

from __future__ import annotations

from office365.directory.identitygovernance.entitlementmanagement.identity_source import IdentitySource
from office365.intune.devices.compliance.policy import DeviceCompliancePolicy
from office365.migration.offline import offline_context
from office365.onedrive.filestorage.containers.container import FileStorageContainer
from office365.runtime.odata.v4.json_format import V4JsonFormat
from office365.search.answers.answer import SearchAnswer
from office365.search.answers.state import AnswerState


def test_a_container_names_the_type_the_catalog_declares():
    """``graph.fileStorageContainer`` was the only entity type name outside the namespace."""
    container = FileStorageContainer(offline_context())

    assert container.entity_type_name == "microsoft.graph.FileStorageContainer"


def test_a_search_answer_answers_the_state_every_subtype_declares():
    answer = SearchAnswer(offline_context())
    assert answer.state is AnswerState.published

    answer.set_property("state", AnswerState.draft)
    assert answer.state is AnswerState.draft
    # ``searchAnswer`` does not declare it: the subtypes do, which is what ``system`` says.
    assert "state" in SearchAnswer._schema.system


def test_a_compliance_policy_answers_the_version_bounds_its_subtypes_declare():
    policy = DeviceCompliancePolicy(offline_context())
    assert policy.os_minimum_version is None and policy.os_maximum_version is None

    policy.set_property("osMaximumVersion", "10.0.19045")
    assert policy.to_json(V4JsonFormat("none")) == {"osMaximumVersion": "10.0.19045"}


def test_an_identity_source_carries_the_name_every_subtype_declares():
    source = IdentitySource(displayName="contoso")

    assert source.entity_type_name == "microsoft.graph.IdentitySource"
    assert source.to_json(V4JsonFormat("none")) == {"displayName": "contoso"}
