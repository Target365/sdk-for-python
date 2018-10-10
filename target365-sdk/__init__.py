from helpers.http_client import HttpClient
from helpers.http_error_handler import HttpErrorHandler
from models.lookup_result import LookupResult
from models.keyword import Keyword
from models.out_message import OutMessage
from models.strex_merchant_id import StrexMerchantId

name = "target365-sdk"


class ApiClient:
    PING = "api/ping"
    LOOKUP = "api/lookup"
    KEYWORDS = "api/keywords"
    OUT_MESSAGES = "api/out-messages"
    STREX_MERCHANTS = "api/strex/merchants"

    NOT_FOUND = 404

    def __init__(self, baseUri, keyName, privateKey):
        self.client = HttpClient(baseUri, keyName, privateKey)
        self.errorHandler = HttpErrorHandler()

    # Ping controller
    def Ping(self):
        """
          Pings the service and returns a hello message
          :return: return description
        """
        response = self.client.get(self.PING)
        self.errorHandler.throwIfNotSuccess(response)
        return response.text # returns the string "pong"

    # Lookup controller

    def Lookup(self, msisdn):
        """
        Looks up address info on a mobile phone number.
        :msisdn: Mobile phone number (required)
        :return: LookupResult
        """

        if msisdn is None:
            raise ValueError("msisdn")
        payload = {"msisdn": msisdn}
        response = self.client.getWithParams(self.LOOKUP, payload)
        if response.status_code == self.NOT_FOUND:
            return None
        self.errorHandler.throwIfNotSuccess(response)
        lookupResult = LookupResult()
        lookupResult.fromDict(response.json())
        return lookupResult

    # Keyword controller

    def CreateKeyword(self, keyword):
        """
        Creates a new keyword.
        :keyword: Keyword
        :return: string
        """
        if keyword is None:
            raise ValueError("keyword")
        response = self.client.post(self.KEYWORDS, keyword)
        self.errorHandler.throwIfNotSuccess(response)

        return self._getIdFromHeader(response.headers)

    def GetAllKeywords(self, shortNumberId=None, keyword=None, mode=None, tag=None):
        """
        Gets all keywords.
        :return: Keyword[]
        """
        params = {}
        if shortNumberId is not None:
            params["shortNumberId"] = shortNumberId
        if keyword is not None:
            params["keywordText"] = keyword
        if mode is not None:
            params["mode"] = mode
        if tag is not None:
            params["tag"] = tag

        response = self.client.getWithParams(self.KEYWORDS, params)
        self.errorHandler.throwIfNotSuccess(response)
        return Keyword().fromResponseList(response.json())

    def GetKeyword(self, keywordId):
        """
        Gets a keyword.
        :keywordId: string
        :return: Keyword
        """
        if keywordId is None:
            raise ValueError("keywordId")

        response = self.client.get(self.KEYWORDS + "/" + keywordId)
        if response.status_code == self.NOT_FOUND:
            return None

        self.errorHandler.throwIfNotSuccess(response)
        
        keyword = Keyword()
        keyword.fromDict(response.json())
        return keyword

    def UpdateKeyword(self, keyword):
        """
        Updates a keywrod
        :keyword: Keyword to update      
        """
        if keyword is None:
            raise ValueError("keyword")
        if keyword.keywordId is None:
            raise ValueError("keywordId")

        response = self.client.put(
            self.KEYWORDS + "/" + keyword.keywordId, keyword)

        self.errorHandler.throwIfNotSuccess(response)

    def DeleteKeyword(self, keywordId):
        """
        Deletes a keyword
        :keywordId: string
        """
        if keywordId is None:
            raise ValueError("keywordId")

        response = self.client.delete(self.KEYWORDS + "/" + keywordId)
        self.errorHandler.throwIfNotSuccess(response)

    # OutMessage controller

    def CreateOutMessage(self, message):
        """
        Creates a new out-message
        :message: OutMessage
        """
        if message is None:
            raise ValueError("message")

        response = self.client.post(self.OUT_MESSAGES, message)
        self.errorHandler.throwIfNotSuccess(response)

        return self._getIdFromHeader(response.headers)

    def CreateOutMessageBatch(self, messages):
        """
        Creates a new out-message batch.
        :messages: OutMessage[]
        """
        if messages is None:
            raise ValueError("messages")

        response = self.client.post(self.OUT_MESSAGES + "/batch", messages)
        self.errorHandler.throwIfNotSuccess(response)

    def GetOutMessage(self, transactionId):
        """
        Gets and out-message
        :transactionId: string
        :return: OutMessage
        """
        if transactionId is None:
            raise ValueError("transactionId")

        response = self.client.get(self.OUT_MESSAGES + "/" + transactionId)
        if response.status_code == self.NOT_FOUND:
            return None

        self.errorHandler.throwIfNotSuccess(response)
        outMessage = OutMessage()
        outMessage.fromDict(response.json())
        return outMessage

    def UpdateOutMessage(self, message):
        """
        Updates a future scheduled out-message.
        :message: OutMessage
        """
        if message is None:
            raise ValueError("message")
        if message.transactionId is None:
            raise ValueError("transactionId")

        response = self.client.put(
            self.OUT_MESSAGES + "/" + message.transactionId, message)
        self.errorHandler.throwIfNotSuccess(response)

    def DeleteOutMessage(self, transactionId):
        """
        Deletes a future sheduled out-message.
        :transactionId: string
        """
        if transactionId is None:
            raise ValueError("transactionId")

        response = self.client.delete(self.OUT_MESSAGES + "/" + transactionId)
        self.errorHandler.throwIfNotSuccess(response)

    def ReversePayment(self, transactionId):
        """
        NOT IN SWAGGER SPEC
        Reverses a payment transaction
        This method is idempotent and can be called multiple times without problems.
        :transactionId: string
        :return: string
        """
        if transactionId is None:
            raise ValueError("transactionId")

        response = self.client.get(
            "api/reverse-payment", params={'transactionId': transactionId})
        self.errorHandler.throwIfNotSuccess(response)
        return self._getIdFromHeader(response.headers)

    # StrexMerchantIds controller

    def GetMerchantIds(self):
        """
        Gets all merchant ids.
        :return: string[]
        """
        response = self.client.get(self.STREX_MERCHANTS)
        self.errorHandler.throwIfNotSuccess(response)
        stringList = response.json()
        return stringList

    def GetMerchant(self, merchantId):
        """
        Gets a merchant.
        :merchantId: string
        :returns: StrexMerchantId
        """
        if merchantId is None:
            raise ValueError("merchantId")

        response = self.client.get(self.STREX_MERCHANTS + "/" + merchantId)
        if response.status_code == self.NOT_FOUND:
            return None

        self.errorHandler.throwIfNotSuccess(response)
        strexMerchantId = StrexMerchantId()
        strexMerchantId.fromDict(response.json())
        return strexMerchantId

    def SaveMerchant(self, merchant):
        """
        Creates/updates a merchant.
        :merchant: StrexMerchantId
        """
        if merchant is None:
            raise ValueError("merchant")
        if merchant.merchantId is None:
            raise ValueError("merchantId")

        response = self.client.put(self.STREX_MERCHANTS + "/" + merchant.merchantId, merchant)
        self.errorHandler.throwIfNotSuccess(response)

    def DeleteMerchant(self, merchantId):
        """
        Deletes a merchant
        :merchantId: string
        """
        if merchantId is None:
            raise ValueError("merchantId")

        response = self.client.delete(self.STREX_MERCHANTS + "/" + merchantId)
        self.errorHandler.throwIfNotSuccess(response)
    
    def _getIdFromHeader(self, headers):
        """
        Returns the newly created resource's identifier from the Locaion header
        :returns: resource identifier
        """
        chunks = headers["Location"].split("/")
        return chunks[-1]

baseUri = "https://test.target365.io/"
keyName = "CreologixTest2"
privateKey = "07CC657050F80EE186E2ECD53B39C0DEB28B6F41F3FC0408A8C26F2ECD9A6212"

client = ApiClient(baseUri, keyName, privateKey)

# print(client.Ping())


##### KEYWORDS

# {
#   "keywordId": "123",
#   "shortNumberId": "NO-0000",
#   "keywordText": "Test",
#   "mode": "Text",
#   "forwardUrl": "https://tempuri.org",
#   "enabled": true,
#   "created": "2018-04-12T12:00:00Z",
#   "lastModified": "2018-04-15T14:00:00Z",
#   "tags": [
#     "Foo",
#     "Bar"
#   ]
# }

validShortNumberId = "NO-0000"

keyword = Keyword()
keyword.keywordId = "123"
keyword.shortNumberId = validShortNumberId
keyword.keywordText = "Test11"
keyword.mode = "Wildcard"
keyword.forwardUrl = "https://tempuri.org"
keyword.enabled = True
keyword.created = "2018-04-12T12:00:00Z"
keyword.lastModified = "2018-04-15T14:00:00Z"
keyword.tags = ["Foo","Bar"]
# print(client.CreateKeyword(keyword))
# print(client.GetAllKeywords())
# print(client.GetKeyword("179").shortNumberId)

# keywordToUpdate = client.GetKeyword("179")
# keywordToUpdate.keywordText = "TestUpdated2"
# print(client.UpdateKeyword(keywordToUpdate))

# print(client.GetKeyword("177"))
# print(client.DeleteKeyword("177"))

####### Out Messages

{
  "transactionId": "8eb5e79d-0b3d-4e50-a4dd-7a939af4c4c3",
  "correlationId": "12345",
  "sender": "0000",
  "recipient": "+4798079008",
  "content": "Hi! This is a message from 0000 :)",
  "sendTime": "2018-04-12T13:27:50Z",
  "timeToLive": 120,
  "priority": "Normal",
  "deliveryMode": "AtMostOnce",
  "deliveryReportUrl": "https://tempuri.org",
  "lastModified": "2018-04-12T12:00:00Z",
  "created": "2018-04-12T12:00:00Z",
  "tags": []
}

outMessage = OutMessage()
outMessage.sender = "0000"
outMessage.recipient = "+4798079008"
outMessage.content = "Hi! This is a message from 0000 :)"
outMessage.sendTime = "2018-10-12T12:00:00Z" # if omitted, sends right away

# outMessageId = client.CreateOutMessage(outMessage)
# print(outMessageId)
# fetchedOutMessage = client.GetOutMessage(outMessageId)
# fetchedOutMessage.content += fetchedOutMessage.content
# client.UpdateOutMessage(fetchedOutMessage)
# fetchedOutMessage = client.GetOutMessage(outMessageId)
# print(fetchedOutMessage.content)
# client.DeleteOutMessage(outMessageId)
# print(client.GetOutMessage(outMessageId))

# outMessage1 = OutMessage()
# outMessage1.transactionId = "a9522701-5e33-4593-9014-19dfb4a7ee7f"
# outMessage1.sender = "0000"
# outMessage1.recipient = "+4798079008"
# outMessage1.content = "Hi! This is a message from 0000 :)"
# outMessage1.sendTime = "2018-10-12T12:00:00Z" # if omitted, sends right away
# outMessage2 = OutMessage()
# outMessage2.transactionId = "206d4783-ddec-468f-9b9f-588ff6d75b04"
# outMessage2.sender = "0000"
# outMessage2.recipient = "+4798079008"
# outMessage2.content = "Hi! This is a message from 0000 :)"
# outMessage2.sendTime = "2018-10-12T12:00:00Z" # if omitted, sends right away
# outMessage3 = OutMessage()
# outMessage3.transactionId = "a81ca119-3dde-4896-a4d8-08711be4456c"
# outMessage3.sender = "0000"
# outMessage3.recipient = "+4798079008"
# outMessage3.content = "Hi! This is a message from 0000 :)"
# outMessage3.sendTime = "2018-10-12T12:00:00Z" # if omitted, sends right away
# messages = [outMessage1, outMessage2, outMessage3]
# print(client.CreateOutMessageBatch(messages))

# merchantId = StrexMerchantId()
# merchantId.merchantId = "12341"
# merchantId.shortNumberId = validShortNumberId
# print(client.SaveMerchant(merchantId))
# print(client.GetMerchantIds())

# print(client.Lookup("+4798079008"))