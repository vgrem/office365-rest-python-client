from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.migrationcenter.taskupdateresult import TaskUpdateResult


class BatchUpdateResult(ClientValue):

    def __init__(
        self,
        error_code: str = None,
        fail_count: int = None,
        processing_milliseconds: int = None,
        result_list: ClientValueCollection[TaskUpdateResult] = ClientValueCollection(
            TaskUpdateResult
        ),
        success_count: int = None,
    ):
        self.ErrorCode = error_code
        self.FailCount = fail_count
        self.ProcessingMilliseconds = processing_milliseconds
        self.ResultList = result_list
        self.SuccessCount = success_count

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.MigrationCenter.Common.BatchUpdateResult"
