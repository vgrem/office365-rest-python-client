from enum import Enum


class FileHashType(Enum):
    unknown = "0"
    sha1 = "1"
    sha256 = "2"
    md5 = "3"
    authenticodeHash256 = "4"
    lsHash = "5"
    ctph = "6"
    unknownFutureValue = "127"

    @property
    def entity_type_name(self):
        return "microsoft.graph.FileHashType"
