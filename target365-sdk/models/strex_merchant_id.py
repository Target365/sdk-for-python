class StrexMerchantId:
    def from_dict(self, dictionary_item):
        self.merchantId = dictionary_item["merchantId"]
        self.shortNumberId = dictionary_item["shortNumberId"]
        self.password = dictionary_item["password"]
    
    def from_response_list(self, list_of_strex_merchant_ids):
        items = []
        for item in list_of_strex_merchant_ids:
            strexMerchantId = StrexMerchantId()
            strexMerchantId.from_dict(item)
            items.append(strexMerchantId)

        return items
