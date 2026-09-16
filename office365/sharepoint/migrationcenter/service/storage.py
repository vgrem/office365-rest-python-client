from typing import Optional

from typing_extensions import Self

from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.sharepoint.entity import Entity
from office365.sharepoint.migrationcenter.storagesettings import MigrationStorageSettings
from office365.sharepoint.migrationcenter.taskschedulerinformation import TaskSchedulerInformation
from office365.sharepoint.migrationcenter.tasksettings import MigrationTaskSettings


class MigrationCenterStorage(Entity):
    """ """

    def __init__(self, context, resource_path=None):
        if resource_path is None:
            resource_path = ResourcePath("Microsoft.Online.SharePoint.MigrationCenter.Service.MigrationCenterStorage")
        super().__init__(context, resource_path)

    @property
    def action_id(self) -> Optional[int]:
        """Gets the ActionId property"""
        return self.properties.get("ActionId", None)

    @property
    def debug_command(self) -> Optional[str]:
        """Gets the DebugCommand property"""
        return self.properties.get("DebugCommand", None)

    @property
    def device_count(self) -> Optional[int]:
        """Gets the DeviceCount property"""
        return self.properties.get("DeviceCount", None)

    @property
    def global_task_settings(self) -> MigrationTaskSettings:
        """Gets the GlobalTaskSettings property"""
        return self.properties.get("GlobalTaskSettings", MigrationTaskSettings())

    @property
    def is_service_initialized(self) -> Optional[bool]:
        """Gets the IsServiceInitialized property"""
        return self.properties.get("IsServiceInitialized", None)

    @property
    def performance_data_count(self) -> Optional[int]:
        """Gets the PerformanceDataCount property"""
        return self.properties.get("PerformanceDataCount", None)

    @property
    def scheduler_information(self) -> TaskSchedulerInformation:
        """Gets the SchedulerInformation property"""
        return self.properties.get("SchedulerInformation", TaskSchedulerInformation())

    @property
    def schema_version(self) -> Optional[str]:
        """Gets the SchemaVersion property"""
        return self.properties.get("SchemaVersion", None)

    @property
    def task_count(self) -> Optional[int]:
        """Gets the TaskCount property"""
        return self.properties.get("TaskCount", None)

    @property
    def total_devices_added(self) -> Optional[int]:
        """Gets the TotalDevicesAdded property"""
        return self.properties.get("TotalDevicesAdded", None)

    @property
    def total_performance_data_added(self) -> Optional[int]:
        """Gets the TotalPerformanceDataAdded property"""
        return self.properties.get("TotalPerformanceDataAdded", None)

    @property
    def total_tasks_added(self) -> Optional[int]:
        """Gets the TotalTasksAdded property"""
        return self.properties.get("TotalTasksAdded", None)

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.MigrationCenter.Service.MigrationCenterStorage"

    def create(self, config: MigrationStorageSettings) -> Self:
        """Create operation.

        Args:
            config (MigrationStorageSettings): config parameter
        """
        qry = ServiceOperationQuery(self, "Create", None, {"config": config}, None, None)
        self.context.add_query(qry)
        return self

    def file(self, folder_name: str, file_name: str, file: bytes, overwrite: bool) -> Self:
        """File operation.

        Args:
            folder_name (str): folderName parameter
            file_name (str): fileName parameter
            file (bytes): file parameter
            overwrite (bool): overwrite parameter
        """
        qry = ServiceOperationQuery(
            self,
            "File",
            None,
            {"folderName": folder_name, "fileName": file_name, "file": file, "overwrite": overwrite},
            None,
            None,
        )
        self.context.add_query(qry)
        return self
