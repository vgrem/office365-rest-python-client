from __future__ import annotations

from typing import Optional

from office365.directory.identitygovernance.lifecycletaskcategory import LifecycleTaskCategory
from office365.directory.identitygovernance.task_processing_result import TaskProcessingResult
from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.key_value_pair import KeyValuePair


class Task(Entity):
    @property
    def arguments(self) -> ClientValueCollection[KeyValuePair]:
        """Gets the arguments property"""
        return self.properties.get("arguments", ClientValueCollection[KeyValuePair](KeyValuePair))

    @property
    def category(self) -> LifecycleTaskCategory:
        """Gets the category property"""
        return self.properties.get("category", LifecycleTaskCategory.joiner)

    @property
    def continue_on_error(self) -> Optional[bool]:
        """Gets the continueOnError property"""
        return self.properties.get("continueOnError", None)

    @property
    def description(self) -> Optional[str]:
        """Gets the description property"""
        return self.properties.get("description", None)

    @property
    def display_name(self) -> Optional[str]:
        """Gets the displayName property"""
        return self.properties.get("displayName", None)

    @property
    def execution_sequence(self) -> Optional[int]:
        """Gets the executionSequence property"""
        return self.properties.get("executionSequence", None)

    @property
    def is_enabled(self) -> Optional[bool]:
        """Gets the isEnabled property"""
        return self.properties.get("isEnabled", None)

    @property
    def task_definition_id(self) -> Optional[str]:
        """Gets the taskDefinitionId property"""
        return self.properties.get("taskDefinitionId", None)

    @property
    def task_processing_results(self) -> EntityCollection[TaskProcessingResult]:
        """Gets the taskProcessingResults property"""
        return self.properties.get(
            "taskProcessingResults",
            EntityCollection[TaskProcessingResult](
                self.context, TaskProcessingResult, ResourcePath("taskProcessingResults", self.resource_path)
            ),
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.identityGovernance.Task"
