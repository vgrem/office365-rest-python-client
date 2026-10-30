from __future__ import annotations

from office365.entity import Entity
from office365.runtime.types.odata_property import odata
from office365.security.cases.reviewsetsettings import ReviewSetSettings
from office365.security.cases.type import CaseType
from office365.security.ocr_settings import OcrSettings
from office365.security.redundancy_detection_settings import RedundancyDetectionSettings
from office365.security.topic_modeling_settings import TopicModelingSettings


class EdiscoveryCaseSettings(Entity):
    @odata(name="caseType")
    @property
    def case_type(self) -> CaseType:
        """Gets the caseType property"""
        return self.properties.get("caseType", CaseType.standard)

    @odata(name="reviewSetSettings")
    @property
    def review_set_settings(self) -> ReviewSetSettings:
        """Gets the reviewSetSettings property"""
        return self.properties.get("reviewSetSettings", ReviewSetSettings.none)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.EdiscoveryCaseSettings"

    @odata(name="ocr")
    @property
    def ocr(self) -> OcrSettings:
        """Gets the ocr property"""
        return self.properties.get("ocr", OcrSettings())

    @odata(name="redundancyDetection")
    @property
    def redundancy_detection(self) -> RedundancyDetectionSettings:
        """Gets the redundancyDetection property"""
        return self.properties.get("redundancyDetection", RedundancyDetectionSettings())

    @odata(name="topicModeling")
    @property
    def topic_modeling(self) -> TopicModelingSettings:
        """Gets the topicModeling property"""
        return self.properties.get("topicModeling", TopicModelingSettings())
