class OutMessage:
    def fromDict(self, dictionnaryItem):
        self.transactionId = dictionnaryItem["transactionId"]
        self.correlationId = dictionnaryItem["correlationId"]
        self.keywordId = dictionnaryItem["keywordId"]
        self.sender = dictionnaryItem["sender"]
        self.recipient = dictionnaryItem["recipient"]
        self.content = dictionnaryItem["content"]
        self.sendTime = dictionnaryItem["sendTime"]
        self.timeToLive = dictionnaryItem["timeToLive"]
        self.priority = dictionnaryItem["priority"]
        self.deliveryMode = dictionnaryItem["deliveryMode"]
        
        # only used for STREX messages
        self.merchantId = dictionnaryItem.get("merchantId", None)
        self.serviceCode = dictionnaryItem.get("serviceCode", None)
        self.invoiceText = dictionnaryItem.get("invoiceText", None)
        self.price = dictionnaryItem.get("price", None)
        
        self.deliveryReportUrl = dictionnaryItem["deliveryReportUrl"]
        self.lastModified = dictionnaryItem["lastModified"]
        self.created = dictionnaryItem["created"]
        self.statusCode = dictionnaryItem["statusCode"]
        self.delivered = dictionnaryItem["delivered"]
        self.billed = dictionnaryItem["billed"]
        self.tags = dictionnaryItem["tags"]
