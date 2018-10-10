class StrexMerchantId:
    def fromDict(self, dict):
        self.merchantId = dict["merchantId"]
        self.shortNumberId = dict["shortNumberId"]
        self.password = dict["password"]
