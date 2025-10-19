from enum import Enum


class MiracastChannel(Enum):
    userDefined = "0"
    one = "1"
    two = "2"
    three = "3"
    four = "4"
    five = "5"
    six = "6"
    seven = "7"
    eight = "8"
    nine = "9"
    ten = "10"
    eleven = "11"
    thirtySix = "36"
    forty = "40"
    fortyFour = "44"
    fortyEight = "48"
    oneHundredFortyNine = "149"
    oneHundredFiftyThree = "153"
    oneHundredFiftySeven = "157"
    oneHundredSixtyOne = "161"
    oneHundredSixtyFive = "165"

    @property
    def entity_type_name(self):
        return "microsoft.graph.MiracastChannel"
