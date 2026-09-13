from datetime import datetime
from typing import Optional
from uuid import UUID

from office365.runtime.client_result import ClientResult
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.sharepoint.contentcenter.machinelearning.column_autofill_preview_data import (
    SPMachineLearningColumnAutofillPreviewData,
)
from office365.sharepoint.contentcenter.machinelearning.column_autofill_preview_result import (
    SPMachineLearningColumnAutofillPreviewResult,
)
from office365.sharepoint.contentcenter.machinelearning.list_autofill_entity_data import (
    SPMachineLearningListAutofillEntityData,
)
from office365.sharepoint.contentcenter.machinelearning.list_autofill_item_results import (
    SPMachineLearningListAutofillItemResults,
)
from office365.sharepoint.contentcenter.machinelearning.sp_machine_learning_doc_lib_autofill_item_results import (
    SPMachineLearningDocLibAutofillItemResults,
)
from office365.sharepoint.entity import Entity


class SPMachineLearningWorkItem(Entity):
    @property
    def entity_type_name(self):
        return "Microsoft.Office.Server.ContentCenter.SPMachineLearningWorkItem"

    @property
    def created(self) -> Optional[datetime]:
        """Gets the Created property"""
        return self.properties.get("Created", datetime.min)

    @property
    def deliver_date(self) -> Optional[datetime]:
        """Gets the DeliverDate property"""
        return self.properties.get("DeliverDate", datetime.min)

    @property
    def error_message(self) -> Optional[str]:
        """Gets the ErrorMessage property"""
        return self.properties.get("ErrorMessage", None)

    @property
    def id_(self) -> Optional[UUID]:
        """Gets the ID property"""
        return self.properties.get("ID", None)

    @property
    def status(self) -> Optional[str]:
        """Gets the Status property"""
        return self.properties.get("Status", None)

    @property
    def status_code(self) -> Optional[int]:
        """Gets the StatusCode property"""
        return self.properties.get("StatusCode", None)

    @property
    def target_server_relative_url(self) -> Optional[str]:
        """Gets the TargetServerRelativeUrl property"""
        return self.properties.get("TargetServerRelativeUrl", None)

    @property
    def target_site_id(self) -> Optional[UUID]:
        """Gets the TargetSiteId property"""
        return self.properties.get("TargetSiteId", None)

    @property
    def target_site_url(self) -> Optional[str]:
        """Gets the TargetSiteUrl property"""
        return self.properties.get("TargetSiteUrl", None)

    @property
    def target_unique_id(self) -> Optional[UUID]:
        """Gets the TargetUniqueId property"""
        return self.properties.get("TargetUniqueId", None)

    @property
    def target_web_id(self) -> Optional[UUID]:
        """Gets the TargetWebId property"""
        return self.properties.get("TargetWebId", None)

    @property
    def target_web_server_relative_url(self) -> Optional[str]:
        """Gets the TargetWebServerRelativeUrl property"""
        return self.properties.get("TargetWebServerRelativeUrl", None)

    @property
    def type_(self) -> Optional[UUID]:
        """Gets the Type property"""
        return self.properties.get("Type", None)

    def autofill_doc_lib_synchronous(
        self, parameters: SPMachineLearningListAutofillEntityData
    ) -> ClientResult[SPMachineLearningDocLibAutofillItemResults]:
        """AutofillDocLibSynchronous operation.

        Args:
            parameters (SPMachineLearningListAutofillEntityData): parameters parameter
        """
        return_type = ClientResult(self.context, SPMachineLearningDocLibAutofillItemResults())
        qry = ServiceOperationQuery(
            self, "AutofillDocLibSynchronous", None, {"parameters": parameters}, None, return_type
        )
        self.context.add_query(qry)
        return return_type

    def autofill_list_synchronous(
        self, parameters: SPMachineLearningListAutofillEntityData
    ) -> ClientResult[SPMachineLearningListAutofillItemResults]:
        """AutofillListSynchronous operation.

        Args:
            parameters (SPMachineLearningListAutofillEntityData): parameters parameter
        """
        return_type = ClientResult(self.context, SPMachineLearningListAutofillItemResults())
        qry = ServiceOperationQuery(self, "AutofillListSynchronous", None, {"parameters": parameters}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def autofill_test_prompt(
        self, parameters: SPMachineLearningColumnAutofillPreviewData
    ) -> ClientResult[SPMachineLearningColumnAutofillPreviewResult]:
        """AutofillTestPrompt operation.

        Args:
            parameters (SPMachineLearningColumnAutofillPreviewData): parameters parameter
        """
        return_type = ClientResult(self.context, SPMachineLearningColumnAutofillPreviewResult())
        qry = ServiceOperationQuery(self, "AutofillTestPrompt", None, {"parameters": parameters}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def create_doc_lib_autofill(self, parameters: SPMachineLearningListAutofillEntityData) -> ClientResult[str]:
        """CreateDocLibAutofill operation.

        Args:
            parameters (SPMachineLearningListAutofillEntityData): parameters parameter
        """
        return_type = ClientResult(self.context, str())
        qry = ServiceOperationQuery(self, "CreateDocLibAutofill", None, {"parameters": parameters}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def create_list_autofill(self, parameters: SPMachineLearningListAutofillEntityData) -> ClientResult[str]:
        """CreateListAutofill operation.

        Args:
            parameters (SPMachineLearningListAutofillEntityData): parameters parameter
        """
        return_type = ClientResult(self.context, str())
        qry = ServiceOperationQuery(self, "CreateListAutofill", None, {"parameters": parameters}, None, return_type)
        self.context.add_query(qry)
        return return_type
