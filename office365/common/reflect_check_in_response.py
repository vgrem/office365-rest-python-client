from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.education.responseemotiontype import ResponseEmotionType
    from office365.education.responsefeedbacktype import ResponseFeedbackType


class ReflectCheckInResponse(Entity):
    @odata(name="checkInId")
    @property
    def check_in_id(self) -> Optional[str]:
        """Gets the checkInId property"""
        return self.properties.get("checkInId", None)

    @odata(name="checkInTitle")
    @property
    def check_in_title(self) -> Optional[str]:
        """Gets the checkInTitle property"""
        return self.properties.get("checkInTitle", None)

    @odata(name="classId")
    @property
    def class_id(self) -> Optional[str]:
        """Gets the classId property"""
        return self.properties.get("classId", None)

    @odata(name="createdDateTime")
    @property
    def created_date_time(self) -> Optional[datetime]:
        """Gets the createdDateTime property"""
        return self.properties.get("createdDateTime", datetime.min)

    @odata(name="creatorId")
    @property
    def creator_id(self) -> Optional[str]:
        """Gets the creatorId property"""
        return self.properties.get("creatorId", None)

    @odata(name="isClosed")
    @property
    def is_closed(self) -> Optional[bool]:
        """Gets the isClosed property"""
        return self.properties.get("isClosed", None)

    @odata(name="responderId")
    @property
    def responder_id(self) -> Optional[str]:
        """Gets the responderId property"""
        return self.properties.get("responderId", None)

    @odata(name="responseEmotion")
    @property
    def response_emotion(self) -> ResponseEmotionType:
        """Gets the responseEmotion property"""
        from office365.education.responseemotiontype import ResponseEmotionType

        return self.properties.get("responseEmotion", ResponseEmotionType.none)

    @odata(name="responseFeedback")
    @property
    def response_feedback(self) -> ResponseFeedbackType:
        """Gets the responseFeedback property"""
        from office365.education.responsefeedbacktype import ResponseFeedbackType

        return self.properties.get("responseFeedback", ResponseFeedbackType.none)

    @odata(name="submitDateTime")
    @property
    def submit_date_time(self) -> Optional[datetime]:
        """Gets the submitDateTime property"""
        return self.properties.get("submitDateTime", datetime.min)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ReflectCheckInResponse"
