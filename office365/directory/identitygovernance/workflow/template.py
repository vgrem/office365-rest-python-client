from typing import Optional

from office365.directory.identitygovernance.lifecycleworkflows.category import LifecycleWorkflowCategory
from office365.directory.identitygovernance.task import Task
from office365.directory.identitygovernance.workflow.executionconditions import WorkflowExecutionConditions
from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.runtime.paths.resource_path import ResourcePath


class WorkflowTemplate(Entity):
    """Represents the pre-configured templates of Lifecycle Workflows that are available in Microsoft Entra ID.
    Workflow templates are available for common scenarios such as new hires and users that are leaving the organization.

    Workflow templates allow you to set up workflows based on common lifecycle management scenarios.
    You can also create custom workflows from the workflow templates to achieve specific situations.
    """

    @property
    def category(self) -> LifecycleWorkflowCategory:
        """Gets the category property"""
        return self.properties.get("category", LifecycleWorkflowCategory.joiner)

    @property
    def description(self) -> Optional[str]:
        """Gets the description property"""
        return self.properties.get("description", None)

    @property
    def display_name(self) -> Optional[str]:
        """Gets the displayName property"""
        return self.properties.get("displayName", None)

    @property
    def execution_conditions(self) -> WorkflowExecutionConditions:
        """Gets the executionConditions property"""
        return self.properties.get("executionConditions", WorkflowExecutionConditions())

    @property
    def tasks(self) -> EntityCollection[Task]:
        """Gets the tasks property"""
        return self.properties.get(
            "tasks", EntityCollection[Task](self.context, Task, ResourcePath("tasks", self.resource_path))
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.identityGovernance.WorkflowTemplate"
