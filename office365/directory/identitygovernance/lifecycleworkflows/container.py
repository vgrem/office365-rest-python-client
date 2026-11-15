from __future__ import annotations

from typing import TYPE_CHECKING

from office365.directory.identitygovernance.custom_task_extension import (
    CustomTaskExtension,
)
from office365.directory.identitygovernance.insights import Insights
from office365.directory.identitygovernance.lifecycle_management_settings import (
    LifecycleManagementSettings,
)
from office365.directory.identitygovernance.task_definition import TaskDefinition
from office365.directory.identitygovernance.workflow.template import WorkflowTemplate
from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.directory.identitygovernance.deleted_item_container import (
        DeletedItemContainer,
    )
    from office365.directory.identitygovernance.workflow.workflow import Workflow


class LifecycleWorkflowsContainer(Entity):
    @odata(name="customTaskExtensions", navigation=True)
    @property
    def custom_task_extensions(self) -> EntityCollection[CustomTaskExtension]:
        """Gets the customTaskExtensions property"""
        return self.properties.get(
            "customTaskExtensions",
            EntityCollection[CustomTaskExtension](
                self.context, CustomTaskExtension, ResourcePath("customTaskExtensions", self.resource_path)
            ),
        )

    @odata(name="insights", navigation=True)
    @property
    def insights(self) -> Insights:
        """Gets the insights property"""
        return self.properties.get("insights", Insights(self.context, ResourcePath("insights", self.resource_path)))

    @odata(name="settings", navigation=True)
    @property
    def settings(self) -> LifecycleManagementSettings:
        """Gets the settings property"""
        return self.properties.get(
            "settings", LifecycleManagementSettings(self.context, ResourcePath("settings", self.resource_path))
        )

    @odata(name="taskDefinitions", navigation=True)
    @property
    def task_definitions(self) -> EntityCollection[TaskDefinition]:
        """Gets the taskDefinitions property"""
        return self.properties.get(
            "taskDefinitions",
            EntityCollection[TaskDefinition](
                self.context, TaskDefinition, ResourcePath("taskDefinitions", self.resource_path)
            ),
        )

    @odata(name="workflowTemplates", navigation=True)
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

    @odata(name="deletedItems", navigation=True)
    @property
    def deleted_items(self) -> DeletedItemContainer:
        """Gets the deletedItems property"""
        from office365.directory.identitygovernance.deleted_item_container import (
            DeletedItemContainer,
        )

        return self.properties.get(
            "deletedItems", DeletedItemContainer(self.context, ResourcePath("deletedItems", self.resource_path))
        )

    @odata(name="workflows", navigation=True)
    @property
    def workflows(self) -> EntityCollection[Workflow]:
        """Gets the workflows property"""
        from office365.directory.identitygovernance.workflow.workflow import Workflow

        return self.properties.get(
            "workflows",
            EntityCollection[Workflow](self.context, Workflow, ResourcePath("workflows", self.resource_path)),
        )
