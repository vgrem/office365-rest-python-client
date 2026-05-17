from enum import Enum


class MobileAppContentFileUploadState(Enum):
    success = "0"
    transientError = "1"
    error = "2"
    unknown = "3"
    azureStorageUriRequestSuccess = "100"
    azureStorageUriRequestPending = "101"
    azureStorageUriRequestFailed = "102"
    azureStorageUriRequestTimedOut = "103"
    azureStorageUriRenewalSuccess = "200"
    azureStorageUriRenewalPending = "201"
    azureStorageUriRenewalFailed = "202"
    azureStorageUriRenewalTimedOut = "203"
    commitFileSuccess = "300"
    commitFilePending = "301"
    commitFileFailed = "302"
    commitFileTimedOut = "303"

    @property
    def entity_type_name(self):
        return "microsoft.graph.MobileAppContentFileUploadState"
