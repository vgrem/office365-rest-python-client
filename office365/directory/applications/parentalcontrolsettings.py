from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


class ParentalControlSettings(ClientValue):
    def __init__(self, countries_blocked_for_minors: StringCollection = None, legal_age_group_rule: str = None):
        self.countriesBlockedForMinors = countries_blocked_for_minors
        self.legalAgeGroupRule = legal_age_group_rule

    @property
    def entity_type_name(self):
        return "microsoft.graph.ParentalControlSettings"
