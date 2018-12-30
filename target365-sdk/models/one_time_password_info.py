class OneTimePasswordInfo:
    def fromDict(self, dict):
        self.transactionId = dict['transactionId']
        self.merchantId = dict['merchantId']
        self.recipient = dict['recipient']
        self.recurring = dict['recurring']
        self.sender = dict['sender']
        self.message = dict['message']
        self.timeToLive = dict['timeToLive']
        self.created = dict['created']


