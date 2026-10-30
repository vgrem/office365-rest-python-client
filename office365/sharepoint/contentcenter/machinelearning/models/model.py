from __future__ import annotations

from datetime import datetime
from typing import Optional
from uuid import UUID

from typing_extensions import Self

from office365.runtime.client_result import ClientResult
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.runtime.types.odata_property import odata
from office365.sharepoint.contentcenter.machinelearning.modeldependencies import (
    SPModelDependencies,
)
from office365.sharepoint.contentcenter.machinelearning.modelpublishconfig import (
    SPModelPublishConfig,
)
from office365.sharepoint.entity import Entity


class SPMachineLearningModel(Entity):
    """"""

    @property
    def entity_type_name(self):
        return "Microsoft.Office.Server.ContentCenter.SPMachineLearningModel"

    @odata(name="AIBuilderHybridModelType", beta=True)
    @property
    def ai_builder_hybrid_model_type(self) -> Optional[str]:
        """Gets the AIBuilderHybridModelType property"""
        return self.properties.get("AIBuilderHybridModelType", None)

    @odata(name="AzureCognitivePrebuiltModelName", beta=True)
    @property
    def azure_cognitive_prebuilt_model_name(self) -> Optional[str]:
        """Gets the AzureCognitivePrebuiltModelName property"""
        return self.properties.get("AzureCognitivePrebuiltModelName", None)

    @odata(name="BaseContentTypeName", beta=True)
    @property
    def base_content_type_name(self) -> Optional[str]:
        """Gets the BaseContentTypeName property"""
        return self.properties.get("BaseContentTypeName", None)

    @odata(name="ConfidenceScore", beta=True)
    @property
    def confidence_score(self) -> Optional[str]:
        """Gets the ConfidenceScore property"""
        return self.properties.get("ConfidenceScore", None)

    @odata(name="ContentTypeGroup", beta=True)
    @property
    def content_type_group(self) -> Optional[str]:
        """Gets the ContentTypeGroup property"""
        return self.properties.get("ContentTypeGroup", None)

    @odata(name="ContentTypeId", beta=True)
    @property
    def content_type_id(self) -> Optional[str]:
        """Gets the ContentTypeId property"""
        return self.properties.get("ContentTypeId", None)

    @odata(name="ContentTypeName", beta=True)
    @property
    def content_type_name(self) -> Optional[str]:
        """Gets the ContentTypeName property"""
        return self.properties.get("ContentTypeName", None)

    @odata(name="Created", beta=True)
    @property
    def created(self) -> Optional[datetime]:
        """Gets the Created property"""
        return self.properties.get("Created", datetime.min)

    @odata(name="CreatedBy", beta=True)
    @property
    def created_by(self) -> Optional[str]:
        """Gets the CreatedBy property"""
        return self.properties.get("CreatedBy", None)

    @odata(name="ModelDependencies", beta=True)
    @property
    def model_dependencies(self) -> SPModelDependencies:
        """Gets the ModelDependencies property"""
        return self.properties.get("ModelDependencies", SPModelDependencies())

    @odata(name="DriveId", beta=True)
    @property
    def drive_id(self) -> Optional[str]:
        """Gets the DriveId property"""
        return self.properties.get("DriveId", None)

    @odata(name="Explanations", beta=True)
    @property
    def explanations(self) -> Optional[str]:
        """Gets the Explanations property"""
        return self.properties.get("Explanations", None)

    @odata(name="ExtractorFieldMapping", beta=True)
    @property
    def extractor_field_mapping(self) -> Optional[str]:
        """Gets the ExtractorFieldMapping property"""
        return self.properties.get("ExtractorFieldMapping", None)

    @odata(name="ID", beta=True)
    @property
    def id_(self) -> Optional[int]:
        """Gets the ID property"""
        return self.properties.get("ID", None)

    @odata(name="LastTrained", beta=True)
    @property
    def last_trained(self) -> Optional[datetime]:
        """Gets the LastTrained property"""
        return self.properties.get("LastTrained", datetime.min)

    @odata(name="ListID", beta=True)
    @property
    def list_id(self) -> Optional[UUID]:
        """Gets the ListID property"""
        return self.properties.get("ListID", None)

    @odata(name="ManagementAllowed", beta=True)
    @property
    def management_allowed(self) -> Optional[bool]:
        """Gets the ManagementAllowed property"""
        return self.properties.get("ManagementAllowed", None)

    @odata(name="ModelName", beta=True)
    @property
    def model_name(self) -> Optional[str]:
        """Gets the ModelName property"""
        return self.properties.get("ModelName", None)

    @odata(name="ModelPublishConfig", beta=True)
    @property
    def model_publish_config(self) -> SPModelPublishConfig:
        """Gets the ModelPublishConfig property"""
        return self.properties.get("ModelPublishConfig", SPModelPublishConfig())

    @odata(name="ModelRules", beta=True)
    @property
    def model_rules(self) -> Optional[str]:
        """Gets the ModelRules property"""
        return self.properties.get("ModelRules", None)

    @odata(name="ModelSettings", beta=True)
    @property
    def model_settings(self) -> Optional[str]:
        """Gets the ModelSettings property"""
        return self.properties.get("ModelSettings", None)

    @odata(name="ModelType", beta=True)
    @property
    def model_type(self) -> Optional[int]:
        """Gets the ModelType property"""
        return self.properties.get("ModelType", None)

    @odata(name="ModelTypeAsString", beta=True)
    @property
    def model_type_as_string(self) -> Optional[str]:
        """Gets the ModelTypeAsString property"""
        return self.properties.get("ModelTypeAsString", None)

    @odata(name="ModelTypeInternalName", beta=True)
    @property
    def model_type_internal_name(self) -> Optional[str]:
        """Gets the ModelTypeInternalName property"""
        return self.properties.get("ModelTypeInternalName", None)

    @odata(name="Modified", beta=True)
    @property
    def modified(self) -> Optional[datetime]:
        """Gets the Modified property"""
        return self.properties.get("Modified", datetime.min)

    @odata(name="ModifiedBy", beta=True)
    @property
    def modified_by(self) -> Optional[str]:
        """Gets the ModifiedBy property"""
        return self.properties.get("ModifiedBy", None)

    @odata(name="ObjectId", beta=True)
    @property
    def object_id(self) -> Optional[str]:
        """Gets the ObjectId property"""
        return self.properties.get("ObjectId", None)

    @odata(name="PublicationType", beta=True)
    @property
    def publication_type(self) -> Optional[int]:
        """Gets the PublicationType property"""
        return self.properties.get("PublicationType", None)

    @odata(name="Schemas", beta=True)
    @property
    def schemas(self) -> Optional[str]:
        """Gets the Schemas property"""
        return self.properties.get("Schemas", None)

    @odata(name="SourceSiteUrl", beta=True)
    @property
    def source_site_url(self) -> Optional[str]:
        """Gets the SourceSiteUrl property"""
        return self.properties.get("SourceSiteUrl", None)

    @odata(name="SourceUrl", beta=True)
    @property
    def source_url(self) -> Optional[str]:
        """Gets the SourceUrl property"""
        return self.properties.get("SourceUrl", None)

    @odata(name="SourceWebServerRelativeUrl", beta=True)
    @property
    def source_web_server_relative_url(self) -> Optional[str]:
        """Gets the SourceWebServerRelativeUrl property"""
        return self.properties.get("SourceWebServerRelativeUrl", None)

    @odata(name="UniqueId", beta=True)
    @property
    def unique_id(self) -> Optional[UUID]:
        """Gets the UniqueId property"""
        return self.properties.get("UniqueId", None)

    def add_model_dependency(self, model_id: str, update_existing: bool) -> Self:
        """AddModelDependency operation.

        Args:
            model_id (str): modelId parameter
            update_existing (bool): updateExisting parameter
        """
        qry = ServiceOperationQuery(
            self, "AddModelDependency", None, {"modelId": model_id, "updateExisting": update_existing}, None
        )
        self.context.add_query(qry)
        return self

    def delete(self) -> Self:
        """Delete operation."""
        qry = ServiceOperationQuery(self, "Delete")
        self.context.add_query(qry)
        return self

    def remove_model_dependency(self, model_id: str) -> Self:
        """RemoveModelDependency operation.

        Args:
            model_id (str): modelId parameter
        """
        qry = ServiceOperationQuery(self, "RemoveModelDependency", None, {"modelId": model_id}, None)
        self.context.add_query(qry)
        return self

    def set_as_model_author(self) -> ClientResult[bool]:
        """SetAsModelAuthor operation."""
        return_type = ClientResult(self.context, bool())
        qry = ServiceOperationQuery(self, "SetAsModelAuthor", None, {}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def update_model_settings(self, model_settings: str) -> Self:
        """UpdateModelSettings operation.

        Args:
            model_settings (str): ModelSettings parameter
        """
        qry = ServiceOperationQuery(self, "UpdateModelSettings", None, {"ModelSettings": model_settings}, None)
        self.context.add_query(qry)
        return self

    def update_model_type_specific_settings(self, settings: dict) -> Self:
        """UpdateModelTypeSpecificSettings operation.

        Args:
            settings (dict): Settings parameter
        """
        qry = ServiceOperationQuery(self, "UpdateModelTypeSpecificSettings", None, {"Settings": settings}, None)
        self.context.add_query(qry)
        return self

    @odata(name="ID", beta=True)
    @property
    def id(self) -> Optional[int]:
        """Gets the ID property"""
        return self.properties.get("ID", None)

    def invoke_connector_query(self) -> ClientResult[bytes]:
        """InvokeConnectorQuery operation."""
        return_type = ClientResult(self.context, bytes())
        qry = ServiceOperationQuery(self, "InvokeConnectorQuery", None, {}, None, return_type)
        self.context.add_query(qry)
        return return_type
