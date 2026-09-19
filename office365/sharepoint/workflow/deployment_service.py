from datetime import datetime
from uuid import UUID

from typing_extensions import Self

from office365.runtime.client_result import ClientResult
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.sharepoint.entity import Entity
from office365.sharepoint.entity_collection import EntityCollection
from office365.sharepoint.workflow.definition import WorkflowDefinition


class WorkflowDeploymentService(Entity):
    """"""

    def get_definition(self, definition_id):
        """Returns a WorkflowDefinition from the workflow store."""
        return_type = WorkflowDefinition(self.context)
        payload = {"definitionId": definition_id}
        qry = ServiceOperationQuery(self, "GetDefinition", None, payload, None, return_type)
        self.context.add_query(qry)
        return return_type

    def enumerate_definitions(self, published_only=False):
        """Returns the WorkflowDefinition objects from the workflow store that match the specified parameters."""
        return_type = EntityCollection(self.context, WorkflowDefinition)
        payload = {"publishedOnly": published_only}
        qry = ServiceOperationQuery(self, "EnumerateDefinitions", None, payload, None, return_type)
        self.context.add_query(qry)
        return return_type

    @property
    def entity_type_name(self):
        return "SP.WorkflowServices.WorkflowDeploymentService"

    def delete_collateral(self, workflow_definition_id: UUID, leaf_file_name: str) -> Self:
        """DeleteCollateral operation.

        Args:
            workflow_definition_id (UUID): workflowDefinitionId parameter
            leaf_file_name (str): leafFileName parameter
        """
        qry = ServiceOperationQuery(
            self,
            "DeleteCollateral",
            None,
            {"workflowDefinitionId": workflow_definition_id, "leafFileName": leaf_file_name},
            None,
            None,
        )
        self.context.add_query(qry)
        return self

    def delete_definition(self, definition_id: UUID) -> Self:
        """DeleteDefinition operation.

        Args:
            definition_id (UUID): definitionId parameter
        """
        qry = ServiceOperationQuery(self, "DeleteDefinition", None, {"definitionId": definition_id}, None, None)
        self.context.add_query(qry)
        return self

    def deprecate_definition(self, definition_id: UUID) -> Self:
        """DeprecateDefinition operation.

        Args:
            definition_id (UUID): definitionId parameter
        """
        qry = ServiceOperationQuery(self, "DeprecateDefinition", None, {"definitionId": definition_id}, None, None)
        self.context.add_query(qry)
        return self

    def get_activity_signatures(self, last_changed: datetime) -> ClientResult[dict]:
        """GetActivitySignatures operation.

        Args:
            last_changed (datetime): lastChanged parameter
        """
        return_type = ClientResult(self.context, dict())
        qry = ServiceOperationQuery(
            self, "GetActivitySignatures", None, {"lastChanged": last_changed}, None, return_type
        )
        self.context.add_query(qry)
        return return_type

    def get_collateral_uri(self, workflow_definition_id: UUID, leaf_file_name: str) -> ClientResult[str]:
        """GetCollateralUri operation.

        Args:
            workflow_definition_id (UUID): workflowDefinitionId parameter
            leaf_file_name (str): leafFileName parameter
        """
        return_type = ClientResult(self.context, str())
        qry = ServiceOperationQuery(
            self,
            "GetCollateralUri",
            None,
            {"workflowDefinitionId": workflow_definition_id, "leafFileName": leaf_file_name},
            None,
            return_type,
        )
        self.context.add_query(qry)
        return return_type

    def is_integrated_app(self) -> ClientResult[bool]:
        """IsIntegratedApp operation."""
        return_type = ClientResult(self.context, bool())
        qry = ServiceOperationQuery(self, "IsIntegratedApp", None, {}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def package_definition(
        self, definition_id: UUID, package_default_filename: str, package_title: str, package_description: str
    ) -> ClientResult[str]:
        """PackageDefinition operation.

        Args:
            definition_id (UUID): definitionId parameter
            package_default_filename (str): packageDefaultFilename parameter
            package_title (str): packageTitle parameter
            package_description (str): packageDescription parameter
        """
        return_type = ClientResult(self.context, str())
        qry = ServiceOperationQuery(
            self,
            "PackageDefinition",
            None,
            {
                "definitionId": definition_id,
                "packageDefaultFilename": package_default_filename,
                "packageTitle": package_title,
                "packageDescription": package_description,
            },
            None,
            return_type,
        )
        self.context.add_query(qry)
        return return_type

    def publish_definition(self, definition_id: UUID) -> Self:
        """PublishDefinition operation.

        Args:
            definition_id (UUID): definitionId parameter
        """
        qry = ServiceOperationQuery(self, "PublishDefinition", None, {"definitionId": definition_id}, None, None)
        self.context.add_query(qry)
        return self

    def save_collateral(self, workflow_definition_id: UUID, leaf_file_name: str, file_content: bytes) -> Self:
        """SaveCollateral operation.

        Args:
            workflow_definition_id (UUID): workflowDefinitionId parameter
            leaf_file_name (str): leafFileName parameter
            file_content (bytes): fileContent parameter
        """
        qry = ServiceOperationQuery(
            self,
            "SaveCollateral",
            None,
            {
                "workflowDefinitionId": workflow_definition_id,
                "leafFileName": leaf_file_name,
                "fileContent": file_content,
            },
            None,
            None,
        )
        self.context.add_query(qry)
        return self

    def validate_activity(self, activity_xaml: str) -> ClientResult[str]:
        """ValidateActivity operation.

        Args:
            activity_xaml (str): activityXaml parameter
        """
        return_type = ClientResult(self.context, str())
        qry = ServiceOperationQuery(self, "ValidateActivity", None, {"activityXaml": activity_xaml}, None, return_type)
        self.context.add_query(qry)
        return return_type
