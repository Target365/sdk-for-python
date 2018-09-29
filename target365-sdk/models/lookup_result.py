class LookupResult:
    def fromDict(self, dict):
        """
        Covnerts json deserialized dict object into LookupResult
        :dict: dict
        """
        self.mobile = dict["mobile"]
        self.phone = dict["phone"]
        self.firstName = dict["firstName"]
        self.middleName = dict["middleName"]
        self.lastName = dict["lastName"]
        self.streetName = dict["streetName"]
        self.streetNumber = dict["streetNumber"]
        self.streetLetter = dict["streetLetter"]
        self.zipCode = dict["zipCode"]
        self.city = dict["city"]
        self.gender = dict["gender"]
        self.age = dict["age"]
        self.dateOfBirth = dict["dateOfBirth"]
        self.deceasedDate = dict["deceasedDate"]
