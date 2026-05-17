from enum import Enum


class EngagementConversationMessageReactionType(Enum):
    like = "0"
    love = "1"
    celebrate = "2"
    thank = "3"
    laugh = "4"
    sad = "5"
    happy = "6"
    excited = "7"
    smile = "8"
    silly = "9"
    intenseLaugh = "10"
    starStruck = "11"
    goofy = "12"
    thinking = "13"
    surprised = "14"
    mindBlown = "15"
    scared = "16"
    crying = "17"
    shocked = "18"
    angry = "19"
    agree = "20"
    praise = "21"
    takingNotes = "22"
    heartBroken = "23"
    support = "24"
    confirmed = "25"
    watching = "26"
    brain = "27"
    medal = "28"
    bullseye = "29"
    unknownFutureValue = "30"

    @property
    def entity_type_name(self):
        return "microsoft.graph.EngagementConversationMessageReactionType"
