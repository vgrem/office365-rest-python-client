from enum import Enum


class MailDestinationRoutingReason(Enum):
    none = "0"
    mailFlowRule = "1"
    safeSender = "2"
    blockedSender = "3"
    advancedSpamFiltering = "4"
    domainAllowList = "5"
    domainBlockList = "6"
    notInAddressBook = "7"
    firstTimeSender = "8"
    autoPurgeToInbox = "9"
    autoPurgeToJunk = "10"
    autoPurgeToDeleted = "11"
    outbound = "12"
    notJunk = "13"
    junk = "14"
    unknownFutureValue = "15"

    @property
    def entity_type_name(self):
        return "microsoft.graph.MailDestinationRoutingReason"
