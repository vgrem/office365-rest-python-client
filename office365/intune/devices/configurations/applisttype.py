from enum import Enum


class AppListType(Enum):
    none = "0"
    appsInListCompliant = "1"
    appsNotInListCompliant = "2"

    @property
    def entity_type_name(self):
        return "microsoft.graph.AppListType"
