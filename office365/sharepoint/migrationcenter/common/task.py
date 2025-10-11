from office365.runtime.paths.v3.static import StaticPath
from office365.sharepoint.migrationcenter.common.task_entity_data import (
    MigrationTaskEntityData,
)


class MigrationTask(MigrationTaskEntityData):

    def __init__(self, context):
        static_path = StaticPath("Microsoft.Online.SharePoint.MigrationCenter.Service.MigrationTask")
        super().__init__(context, static_path)

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.MigrationCenter.Service.MigrationTask"
