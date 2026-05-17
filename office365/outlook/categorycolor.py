from enum import Enum


class CategoryColor(Enum):
    none = "-1"
    preset0 = "0"
    preset1 = "1"
    preset2 = "2"
    preset3 = "3"
    preset4 = "4"
    preset5 = "5"
    preset6 = "6"
    preset7 = "7"
    preset8 = "8"
    preset9 = "9"
    preset10 = "10"
    preset11 = "11"
    preset12 = "12"
    preset13 = "13"
    preset14 = "14"
    preset15 = "15"
    preset16 = "16"
    preset17 = "17"
    preset18 = "18"
    preset19 = "19"
    preset20 = "20"
    preset21 = "21"
    preset22 = "22"
    preset23 = "23"
    preset24 = "24"

    @property
    def entity_type_name(self):
        return "microsoft.graph.CategoryColor"
