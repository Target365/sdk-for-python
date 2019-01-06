class OutMessage:
    def from_dict(self, dictionary_item):

        self.transactionId = dictionary_item["transactionId"]
        # self.correlationId = dictionaryItem["correlationId"]
        # self.keywordId = dictionaryItem["keywordId"]
        self.sender = dictionary_item["sender"]
        self.recipient = dictionary_item["recipient"]
        self.content = dictionary_item["content"]
        self.sendTime = dictionary_item["sendTime"]
        self.timeToLive = dictionary_item["timeToLive"]
        self.priority = dictionary_item["priority"]
        self.deliveryMode = dictionary_item["deliveryMode"]
        
        # only used for STREX messages
        self.merchantId = dictionary_item.get("merchantId", None)
        self.serviceCode = dictionary_item.get("serviceCode", None)
        self.invoiceText = dictionary_item.get("invoiceText", None)
        self.price = dictionary_item.get("price", None)
        
        # self.deliveryReportUrl = dictionaryItem["deliveryReportUrl"]
        self.lastModified = dictionary_item["lastModified"]
        self.created = dictionary_item["created"]
        self.statusCode = dictionary_item["statusCode"]
        # self.delivered = dictionaryItem["delivered"]
        # self.billed = dictionaryItem["billed"]
        self.tags = dictionary_item["tags"]
