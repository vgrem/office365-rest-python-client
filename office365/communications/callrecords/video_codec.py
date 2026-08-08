from __future__ import annotations

from enum import Enum


class VideoCodec(Enum):
    unknown = "0"
    invalid = "1"
    av1 = "2"
    h263 = "3"
    h264 = "4"
    h264s = "5"
    h264uc = "6"
    h265 = "7"
    rtvc1 = "8"
    rtVideo = "9"
    xrtvc1 = "10"
    unknownFutureValue = "11"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.callRecords.VideoCodec"
