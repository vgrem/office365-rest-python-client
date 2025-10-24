from enum import Enum


class Tone(Enum):
    tone0 = "0"
    tone1 = "1"
    tone2 = "2"
    tone3 = "3"
    tone4 = "4"
    tone5 = "5"
    tone6 = "6"
    tone7 = "7"
    tone8 = "8"
    tone9 = "9"
    star = "10"
    pound = "11"
    a = "12"
    b = "13"
    c = "14"
    d = "15"
    flash = "16"

    @property
    def entity_type_name(self):
        return "microsoft.graph.Tone"
