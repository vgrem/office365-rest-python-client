from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.collections import GuidCollection
from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity

if TYPE_CHECKING:
    from office365.sharepoint.contentcenter.machinelearning.models.columndef import (
        ColumnDef,
    )


class SPMachineLearningModelEntityData(Entity):
    @property
    def entity_type_name(self):
        return "Microsoft.Office.Server.ContentCenter.SPMachineLearningModelEntityData"

    @odata(name="Accuracy", beta=True)
    @property
    def accuracy(self) -> Optional[float]:
        """Gets the Accuracy property"""
        return self.properties.get("Accuracy", None)

    @odata(name="AIBuilderHybridModelEnvironment", beta=True)
    @property
    def ai_builder_hybrid_model_environment(self) -> Optional[str]:
        """Gets the AIBuilderHybridModelEnvironment property"""
        return self.properties.get("AIBuilderHybridModelEnvironment", None)

    @odata(name="AIBuilderHybridModelHostName", beta=True)
    @property
    def ai_builder_hybrid_model_host_name(self) -> Optional[str]:
        """Gets the AIBuilderHybridModelHostName property"""
        return self.properties.get("AIBuilderHybridModelHostName", None)

    @odata(name="AIBuilderHybridModelInTestEnvironment", beta=True)
    @property
    def ai_builder_hybrid_model_in_test_environment(self) -> Optional[bool]:
        """Gets the AIBuilderHybridModelInTestEnvironment property"""
        return self.properties.get("AIBuilderHybridModelInTestEnvironment", None)

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

    @odata(name="AIBuilderHybridModelType", beta=True)
    @property
    def ai_builder_hybrid_model_type(self) -> Optional[str]:
        """Gets the AIBuilderHybridModelType property"""
        return self.properties.get("AIBuilderHybridModelType", None)

    @odata(name="ColumnId", beta=True)
    @property
    def column_id(self) -> Optional[str]:
        """Gets the ColumnId property"""
        return self.properties.get("ColumnId", None)

    @odata(name="ColumnName", beta=True)
    @property
    def column_name(self) -> Optional[str]:
        """Gets the ColumnName property"""
        return self.properties.get("ColumnName", None)

    @odata(name="Columns", beta=True)
    @property
    def columns(self) -> ClientValueCollection[ColumnDef]:
        """Gets the Columns property"""
        from office365.sharepoint.contentcenter.machinelearning.models.columndef import (
            ColumnDef,
        )

        return self.properties.get("Columns", ClientValueCollection[ColumnDef](ColumnDef))

    @odata(name="ColumnType", beta=True)
    @property
    def column_type(self) -> Optional[str]:
        """Gets the ColumnType property"""
        return self.properties.get("ColumnType", None)

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

    @odata(name="Explanations", beta=True)
    @property
    def explanations(self) -> Optional[str]:
        """Gets the Explanations property"""
        return self.properties.get("Explanations", None)

    @odata(name="LastTrained", beta=True)
    @property
    def last_trained(self) -> Optional[datetime]:
        """Gets the LastTrained property"""
        return self.properties.get("LastTrained", datetime.min)

    @odata(name="Locale", beta=True)
    @property
    def locale(self) -> Optional[str]:
        """Gets the Locale property"""
        return self.properties.get("Locale", None)

    @odata(name="ModelName", beta=True)
    @property
    def model_name(self) -> Optional[str]:
        """Gets the ModelName property"""
        return self.properties.get("ModelName", None)

    @odata(name="ModelSettings", beta=True)
    @property
    def model_settings(self) -> Optional[str]:
        """Gets the ModelSettings property"""
        return self.properties.get("ModelSettings", None)

    @odata(name="ModelType", beta=True)
    @property
    def model_type(self) -> Optional[str]:
        """Gets the ModelType property"""
        return self.properties.get("ModelType", None)

    @odata(name="SampleFileUniqueIds", beta=True)
    @property
    def sample_file_unique_ids(self) -> GuidCollection:
        """Gets the SampleFileUniqueIds property"""
        return self.properties.get("SampleFileUniqueIds", GuidCollection())

    @odata(name="Schemas", beta=True)
    @property
    def schemas(self) -> Optional[str]:
        """Gets the Schemas property"""
        return self.properties.get("Schemas", None)

    @odata(name="TableLinkColumns", beta=True)
    @property
    def table_link_columns(self) -> ClientValueCollection[ColumnDef]:
        """Gets the TableLinkColumns property"""
        from office365.sharepoint.contentcenter.machinelearning.models.columndef import (
            ColumnDef,
        )

        return self.properties.get("TableLinkColumns", ClientValueCollection[ColumnDef](ColumnDef))
