class ProvisioningAction:
    """"""

    other = "0"
    create = "1"
    delete = "2"
    disable = "3"
    update = "4"
    stagedDelete = "5"
    unknownFutureValue = "6"

    @property
    def entity_type_name(self):
        return "microsoft.graph.ProvisioningAction"
