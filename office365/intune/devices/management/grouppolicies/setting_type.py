from __future__ import annotations

from enum import Enum


class GroupPolicySettingType(Enum):
    unknown = "0"
    policy = "1"
    account = "2"
    securityOptions = "3"
    userRightsAssignment = "4"
    auditSetting = "5"
    windowsFirewallSettings = "6"
    appLockerRuleCollection = "7"
    dataSourcesSettings = "8"
    devicesSettings = "9"
    driveMapSettings = "10"
    environmentVariables = "11"
    filesSettings = "12"
    folderOptions = "13"
    folders = "14"
    iniFiles = "15"
    internetOptions = "16"
    localUsersAndGroups = "17"
    networkOptions = "18"
    networkShares = "19"
    ntServices = "20"
    powerOptions = "21"
    printers = "22"
    regionalOptionsSettings = "23"
    registrySettings = "24"
    scheduledTasks = "25"
    shortcutSettings = "26"
    startMenuSettings = "27"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.GroupPolicySettingType"
