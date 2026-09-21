from uuid import UUID

from typing_extensions import Self

from office365.runtime.client_result import ClientResult
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.sharepoint.entity import Entity


class SiteContentProcessingInfoProvider(Entity):
    def get_azure_container_token(self):
        return_type = ClientResult(self.context, str())
        qry = ServiceOperationQuery(self, "GetAzureContainerToken", None, None, None, return_type)
        self.context.add_query(qry)
        return return_type

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Client.Search.Administration.SiteContentProcessingInfoProvider"

    def notify_content_processing_status(self, web_id: str, list_id: str, unique_id: str, properties: dict) -> Self:
        """NotifyContentProcessingStatus operation.

        Args:
            web_id (UUID): webId parameter
            list_id (UUID): listId parameter
            unique_id (UUID): uniqueId parameter
            properties (dict): properties parameter
        """
        qry = ServiceOperationQuery(
            self,
            "NotifyContentProcessingStatus",
            None,
            {"webId": web_id, "listId": list_id, "uniqueId": unique_id, "properties": properties},
            None,
            None,
        )
        self.context.add_query(qry)
        return self

    def report_content_processing_status(
        self,
        web_id: UUID,
        list_id: UUID,
        unique_id: UUID,
        azure_container_token_uri: str,
        encryption_key: bytes,
        priority: int,
        error_code: int,
        error_description: str,
    ) -> Self:
        """ReportContentProcessingStatus operation.

        Args:
            web_id (str): webId parameter
            list_id (str): listId parameter
            unique_id (str): uniqueId parameter
            azure_container_token_uri (str): azureContainerTokenUri parameter
            encryption_key (bytes): encryptionKey parameter
            priority (int): priority parameter
            error_code (int): errorCode parameter
            error_description (str): errorDescription parameter
        """
        qry = ServiceOperationQuery(
            self,
            "ReportContentProcessingStatus",
            None,
            {
                "webId": web_id,
                "listId": list_id,
                "uniqueId": unique_id,
                "azureContainerTokenUri": azure_container_token_uri,
                "encryptionKey": encryption_key,
                "priority": priority,
                "errorCode": error_code,
                "errorDescription": error_description,
            },
            None,
            None,
        )
        self.context.add_query(qry)
        return self
