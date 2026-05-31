from __future__ import annotations

from office365.directory.identitygovernance.custom_task_extension import CustomTaskExtension
from office365.directory.identitygovernance.insights import Insights
from office365.directory.identitygovernance.lifecycle_management_settings import LifecycleManagementSettings
from office365.directory.identitygovernance.task_definition import TaskDefinition
from office365.directory.identitygovernance.workflow.template import WorkflowTemplate
from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.runtime.paths.resource_path import ResourcePath


class LifecycleWorkflowsContainer(Entity):
    @property
    def custom_task_extensions(self) -> EntityCollection[CustomTaskExtension]:
        """Gets the customTaskExtensions property"""
        return self.properties.get(
            "customTaskExtensions",
            EntityCollection[CustomTaskExtension](
                self.context, CustomTaskExtension, ResourcePath("customTaskExtensions", self.resource_path)
            ),
        )

    @property
    def insights(self) -> Insights:
        """Gets the insights property"""
        return self.properties.get("insights", Insights(self.context, ResourcePath("insights", self.resource_path)))

    @property
    def settings(self) -> LifecycleManagementSettings:
        """Gets the settings property"""
        return self.properties.get(
            "settings", LifecycleManagementSettings(self.context, ResourcePath("settings", self.resource_path))
        )

    @property
    def task_definitions(self) -> EntityCollection[TaskDefinition]:
        """Gets the taskDefinitions property"""
        return self.properties.get(
            "taskDefinitions",
            EntityCollection[TaskDefinition](
                self.context, TaskDefinition, ResourcePath("taskDefinitions", self.resource_path)
            ),
        )

    @property
    def workflow_templates(self) -> EntityCollection[WorkflowTemplate]:
        """Gets the workflowTemplates property"""
        return self.properties.get(
            "workflowTemplates",
            EntityCollection[WorkflowTemplate](
                self.context, WorkflowTemplate, ResourcePath("workflowTemplates", self.resource_path)
            ),
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.identityGovernance.LifecycleWorkflowsContainer"
