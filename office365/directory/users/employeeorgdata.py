from office365.runtime.client_value import ClientValue


class EmployeeOrgData(ClientValue):

    def __init__(self, cost_center: str = None, division: str = None):
        self.costCenter = cost_center
        self.division = division

    @property
    def entity_type_name(self):
        return "microsoft.graph.EmployeeOrgData"
