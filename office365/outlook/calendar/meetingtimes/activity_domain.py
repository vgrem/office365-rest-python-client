class ActivityDomain:
    """"""

    unknown = "0"
    work = "1"
    personal = "2"
    unrestricted = "3"

    @property
    def entity_type_name(self):
        return "microsoft.graph.ActivityDomain"
