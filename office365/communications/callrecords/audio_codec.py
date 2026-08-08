from __future__ import annotations

from enum import Enum


class AudioCodec(Enum):
    unknown = "0"
    invalid = "1"
    cn = "2"
    pcma = "3"
    pcmu = "4"
    amrWide = "5"
    g722 = "6"
    g7221 = "7"
    g7221c = "8"
    g729 = "9"
    multiChannelAudio = "10"
    muchv2 = "11"
    opus = "12"
    satin = "13"
    satinFullband = "14"
    rtAudio8 = "15"
    rtAudio16 = "16"
    silk = "17"
    silkNarrow = "18"
    silkWide = "19"
    siren = "20"
    xmsRta = "21"
    unknownFutureValue = "22"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.callRecords.AudioCodec"
