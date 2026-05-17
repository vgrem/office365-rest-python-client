from enum import Enum


class AndroidWorkProfileDefaultAppPermissionPolicyType(Enum):
    deviceDefault = "0"
    prompt = "1"
    autoGrant = "2"
    autoDeny = "3"

    @property
    def entity_type_name(self):
        return "microsoft.graph.AndroidWorkProfileDefaultAppPermissionPolicyType"
