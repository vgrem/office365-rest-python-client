from __future__ import annotations

from enum import Enum


class ServiceRole(Enum):
    unknown = "0"
    customBot = "1"
    skypeForBusinessMicrosoftTeamsGateway = "2"
    skypeForBusinessAudioVideoMcu = "3"
    skypeForBusinessApplicationSharingMcu = "4"
    skypeForBusinessCallQueues = "5"
    skypeForBusinessAutoAttendant = "6"
    mediationServer = "7"
    mediationServerCloudConnectorEdition = "8"
    exchangeUnifiedMessagingService = "9"
    mediaController = "10"
    conferencingAnnouncementService = "11"
    conferencingAttendant = "12"
    audioTeleconferencerController = "13"
    skypeForBusinessUnifiedCommunicationApplicationPlatform = "14"
    responseGroupServiceAnnouncementService = "15"
    gateway = "16"
    skypeTranslator = "17"
    skypeForBusinessAttendant = "18"
    responseGroupService = "19"
    voicemail = "20"
    unknownFutureValue = "21"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.callRecords.ServiceRole"
