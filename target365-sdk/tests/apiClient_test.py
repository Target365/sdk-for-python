import unittest
import uuid
from datetime import datetime
from datetime import timedelta
from apiClient import ApiClient
from models.lookup_result import LookupResult
from models.keyword import Keyword
from models.out_message import OutMessage
from models.strex_merchant_id import StrexMerchantId


class Test_TestApiClient(unittest.TestCase):
    baseUri = ""
    keyName = ""
    privateKey = ""
    client = ApiClient(baseUri, keyName, privateKey)

    validShortNumberId = "NO-0000"

    def test_KeywordSequence(self):
        keyword = Keyword()
        keyword.shortNumberId = self.validShortNumberId
        keyword.keywordText = str(uuid.uuid4())
        keyword.mode = "Wildcard"
        keyword.forwardUrl = "https://tempuri.org"
        keyword.enabled = True
        keyword.created = "2018-04-12T12:00:00Z"
        keyword.lastModified = "2018-04-15T14:00:00Z"
        keyword.tags = ["Foo","Bar"]

        # Create a keyword
        createdId = self.client.CreateKeyword(keyword)
        
        # Get the created keyword
        fetchedKeyword = self.client.GetKeyword(str(createdId))
        self.assertEqual(fetchedKeyword.keywordText, keyword.keywordText)

        # Update keyword
        fetchedKeyword.keywordText = str(uuid.uuid4())
        self.client.UpdateKeyword(fetchedKeyword)
        updatedKeyword = self.client.GetKeyword(str(createdId))
        self.assertEqual(updatedKeyword.keywordText, fetchedKeyword.keywordText)

        # Get all with filters returns record
        allKeywords = self.client.GetAllKeywords(self.validShortNumberId, None, "Wildcard", "Foo")
        self.assertGreater(len(allKeywords), 0)

        # Delete
        self.client.DeleteKeyword(str(createdId))

        # Trying to fetch returns None
        self.assertIsNone(self.client.GetKeyword(str(createdId)))

    def test_OutMessageSequence(self):
        tomorrow = self.__addDays(datetime.utcnow(), 1)
        formatted = self.__formatDatetime(tomorrow)

        # create
        outMessage = OutMessage()
        outMessage.sender = "0000"
        outMessage.recipient = "+4798079008"
        outMessage.content = "Hi! This is a message from 0000 :)"
        outMessage.sendTime = formatted
        identifier = self.client.CreateOutMessage(outMessage)

        # get
        fetched = self.client.GetOutMessage(identifier)
        fetched.content += fetched.content

        # update
        self.client.UpdateOutMessage(fetched)
        updated = self.client.GetOutMessage(identifier)
        self.assertEqual(updated.content, fetched.content)

        # delete
        self.client.DeleteOutMessage(identifier)
        self.assertIsNone(self.client.GetOutMessage(identifier))

        # create batch
        t1 = uuid.uuid4()
        t2 = uuid.uuid4()
        t3 = uuid.uuid4()
        outMessage1 = OutMessage()
        outMessage1.transactionId = str(t1)
        outMessage1.sender = "0000"
        outMessage1.recipient = "+4798079008"
        outMessage1.content = "Hi! This is a message from 0000 :)"
        outMessage1.sendTime = formatted
        outMessage2 = OutMessage()
        outMessage2.transactionId = str(t2)
        outMessage2.sender = "0000"
        outMessage2.recipient = "+4798079008"
        outMessage2.content = "Hi! This is a message from 0000 :)"
        outMessage2.sendTime = formatted
        outMessage3 = OutMessage()
        outMessage3.transactionId = str(t3)
        outMessage3.sender = "0000"
        outMessage3.recipient = "+4798079008"
        outMessage3.content = "Hi! This is a message from 0000 :)"
        outMessage3.sendTime = formatted
        messages = [outMessage1, outMessage2, outMessage3]
        self.client.CreateOutMessageBatch(messages)

        self.client.DeleteOutMessage(str(t1))
        self.client.DeleteOutMessage(str(t2))
        self.client.DeleteOutMessage(str(t3))

    def test_PrepareMsisdns(self):
        self.client.PrepareMsisdns(["+4798079008"])        

    def test_LookupShouldReturnResult(self):
        self.assertIsNotNone(self.client.Lookup("+4798079008"))

    def test_StrexMerchantIdSequence(self):
        merchantIdIdentifier = "12341"
        
        # create        
        merchantId = StrexMerchantId()
        merchantId.merchantId = merchantIdIdentifier
        merchantId.shortNumberId = self.validShortNumberId
        merchantId.password = "abcdef"
        self.client.SaveMerchant(merchantId)

        # get by id
        fetched = self.client.GetMerchant(merchantIdIdentifier)
        self.assertIsNotNone(fetched)

        # get all
        self.assertGreater(len(self.client.GetMerchantIds()), 0)

        # delete
        self.client.DeleteMerchant(merchantIdIdentifier)
        self.assertIsNone(self.client.GetMerchant(merchantIdIdentifier))


    # Formats datetime object into utc string
    # got from https://stackoverflow.com/questions/19654578/python-utc-datetime-objects-iso-format-doesnt-include-z-zulu-or-zero-offset
    def __formatDatetime(self, datetime):
        return datetime.strftime('%Y-%m-%dT%H:%M:%S') + datetime.strftime('.%f')[:4] + 'Z'

    def __addDays(self, datetime, daysCount):
        return datetime + timedelta(days=daysCount)

if __name__ == '__main__':
    unittest.main()
