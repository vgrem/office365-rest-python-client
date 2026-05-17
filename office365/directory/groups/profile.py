from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


class GroupProfile(ClientValue):
    def __init__(
        self,
        name: str,
        description: str | None = None,
        mail_enabled: bool = False,
        security_enabled: bool = True,
        group_types: list[str] | None = None,
        owners: list[str] | None = None,
        members: list[str] | None = None,
    ):
        """
        :param str name: The display name for the group
        :param str description: An optional description for the group.
        :param bool mail_enabled: Specifies whether the group is mail-enabled. Default: false
        :param bool security_enabled: Specifies whether the group is a security group. Default: true.
        :param list[str] group_types:
        """
        super().__init__()
        self.mailNickname = name
        self.displayName = name
        self.description = description
        self.mailEnabled = mail_enabled
        self.securityEnabled = security_enabled
        self.owners = owners
        self.members = members
        self.groupTypes = StringCollection(group_types)
