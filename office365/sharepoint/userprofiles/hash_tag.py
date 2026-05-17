from office365.runtime.client_value import ClientValue


class HashTag(ClientValue):
    def __init__(self, name=None, use_count=None):
        """
        The HashTag type specifies a string that is being used as a hash tag and a count of the tags use.

        :param str name: The Name property specifies the hash tag string.
        :param int use_count: The UseCount property specifies the number of times that the hash tag is used.
        """
        self.Name = name
        self.UseCount = use_count

    @property
    def entity_type_name(self):
        return "SP.UserProfiles.HashTag"
