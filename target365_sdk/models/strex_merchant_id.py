from .model import Model

class StrexMerchantId(Model):
    def from_dict(self, dictionary_item):
        self.merchantId = dictionary_item["merchantId"]
        self.shortNumberId = dictionary_item["shortNumberId"]
        self.password = dictionary_item["password"]

    # noinspection PyMethodMayBeStatic
    def from_response_list(self, list_of_strex_merchant_ids):
        items = []
        for item in list_of_strex_merchant_ids:
            strex_merchant_id = StrexMerchantId()
            strex_merchant_id.from_dict(item)
            items.append(strex_merchant_id)

        return items
