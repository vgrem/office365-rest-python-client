from __future__ import annotations

from datetime import datetime
from typing import Optional
from uuid import UUID

from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity


class WorkflowAssociation(Entity):
    """Represents the association of a workflow template with a specific list or content type"""

    @odata(name="AllowManual")
    @property
    def allow_manual(self) -> Optional[bool]:
        """Gets the AllowManual property"""
        return self.properties.get("AllowManual", None)

    @odata(name="AssociationData")
    @property
    def association_data(self) -> Optional[str]:
        """Gets the AssociationData property"""
        return self.properties.get("AssociationData", None)

    @odata(name="AutoStartChange")
    @property
    def auto_start_change(self) -> Optional[bool]:
        """Gets the AutoStartChange property"""
        return self.properties.get("AutoStartChange", None)

    @odata(name="AutoStartCreate")
    @property
    def auto_start_create(self) -> Optional[bool]:
        """Gets the AutoStartCreate property"""
        return self.properties.get("AutoStartCreate", None)

    @odata(name="BaseId")
    @property
    def base_id(self) -> Optional[UUID]:
        """Gets the BaseId property"""
        return self.properties.get("BaseId", None)

    @odata(name="Created")
    @property
    def created(self) -> datetime | None:
        """Gets the Created property"""
        return self.properties.get("Created", None)

    @odata(name="Description")
    @property
    def description(self) -> Optional[str]:
        """Gets the Description property"""
        return self.properties.get("Description", None)

    @odata(name="Enabled")
    @property
    def enabled(self) -> Optional[bool]:
        """Gets the Enabled property"""
        return self.properties.get("Enabled", None)

    @odata(name="HistoryListTitle")
    @property
    def history_list_title(self) -> Optional[str]:
        """Gets the HistoryListTitle property"""
        return self.properties.get("HistoryListTitle", None)

    @odata(name="InstantiationUrl")
    @property
    def instantiation_url(self) -> Optional[str]:
        """Gets the InstantiationUrl property"""
        return self.properties.get("InstantiationUrl", None)

    @odata(name="InternalName")
    @property
    def internal_name(self) -> Optional[str]:
        """Gets the InternalName property"""
        return self.properties.get("InternalName", None)

    @odata(name="IsDeclarative")
    @property
    def is_declarative(self) -> Optional[bool]:
        """Gets the IsDeclarative property"""
        return self.properties.get("IsDeclarative", None)

    @odata(name="ListId")
    @property
    def list_id(self) -> Optional[UUID]:
        """Gets the ListId property"""
        return self.properties.get("ListId", None)

    @odata(name="Modified")
    @property
    def modified(self) -> datetime | None:
        """Gets the Modified property"""
        return self.properties.get("Modified", None)

    @odata(name="Name")
    @property
    def name(self) -> Optional[str]:
        """Gets the Name property"""
        return self.properties.get("Name", None)

    @odata(name="RunningInstances")
    @property
    def running_instances(self) -> Optional[int]:
        """Gets the RunningInstances property"""
        return self.properties.get("RunningInstances", None)

    @odata(name="TaskListTitle")
    @property
    def task_list_title(self) -> Optional[str]:
        """Gets the TaskListTitle property"""
        return self.properties.get("TaskListTitle", None)

    @odata(name="WebId")
    @property
    def web_id(self) -> Optional[UUID]:
        """Gets the WebId property"""
        return self.properties.get("WebId", None)

    @property
    def entity_type_name(self):
        return "SP.Workflow.WorkflowAssociation"

    @odata(name="Id")
    @property
    def id(self) -> Optional[UUID]:
        """Gets the Id property"""
        return self.properties.get("Id", None)
