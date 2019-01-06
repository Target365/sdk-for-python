class LookupResult:
    def from_dict(self, dictonary_item):
        """
        Covnerts json deserialized dict object into LookupResult
        :dict: dict
        """
        self.created = dictonary_item["created"]
        self.msisdn = dictonary_item["msisdn"]
        self.landline = dictonary_item["landline"]
        self.firstName = dictonary_item["firstName"]
        self.middleName = dictonary_item["middleName"]
        self.lastName = dictonary_item["lastName"]
        self.companyName = dictonary_item["companyName"]
        self.companyOrgNo = dictonary_item["companyOrgNo"]
        self.streetName = dictonary_item["streetName"]
        self.streetNumber = dictonary_item["streetNumber"]
        self.streetLetter = dictonary_item["streetLetter"]
        self.zipCode = dictonary_item["zipCode"]
        self.city = dictonary_item["city"]
        self.gender = dictonary_item["gender"]
        self.dateOfBirth = dictonary_item["dateOfBirth"]
        self.age = dictonary_item["age"]
        self.deceasedDate = dictonary_item["deceasedDate"]
