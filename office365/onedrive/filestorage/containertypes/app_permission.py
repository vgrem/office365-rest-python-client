from office365.runtime.client_value import ClientValue


class FileStorageContainerTypeAppPermission(ClientValue):
    none = "0"
    readContent = "1"
    writeContent = "2"
    manageContent = "3"
    create = "4"
    delete = "5"
    read = "6"
    write = "7"
    enumeratePermissions = "8"
    addPermissions = "9"
    updatePermissions = "10"
    deletePermissions = "11"
    deleteOwnPermission = "12"
    managePermissions = "13"
    full = "14"
    unknownFutureValue = "15"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.FileStorageContainerTypeAppPermission"
