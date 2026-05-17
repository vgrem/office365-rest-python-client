from enum import Enum


class UsageRights(Enum):
    unknown = "1"
    docEdit = "2"
    edit = "4"
    comment = "8"
    export = "16"
    forward = "32"
    owner = "64"
    print = "128"
    reply = "256"
    replyAll = "512"
    view = "1024"
    extract = "2048"
    viewRightsData = "4096"
    editRightsData = "8192"
    objModel = "16384"
    accessDenied = "32768"
    userDefinedProtectionTypeNotSupportedException = "65536"
    encryptedProtectionTypeNotSupportedException = "131072"
    purviewClaimsChallengeNotSupportedException = "262144"
    exception = "524288"
    unknownFutureValue = "1048576"

    @property
    def entity_type_name(self):
        return "microsoft.graph.UsageRights"
