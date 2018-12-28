import pytest
import os
import uuid
from datetime import datetime
from datetime import timedelta
from apiClient import ApiClient
from models.lookup_result import LookupResult
from models.keyword import Keyword
from models.out_message import OutMessage
from models.strex_merchant_id import StrexMerchantId


@pytest.fixture
def validShortNumberId():
    return 'NO-0000'

@pytest.fixture
def client():
    baseUri = "https://test.target365.io/"
    keyName = os.environ['API_KEY_NAME']
    privateKey = os.environ['API_PRIVATE_KEY']

    client = ApiClient(baseUri, keyName, privateKey)

    return client


def test_KeywordSequence(client, validShortNumberId):
    keyword = Keyword()
    keyword.shortNumberId = validShortNumberId
    keyword.keywordText = str(uuid.uuid4())
    keyword.mode = "Wildcard"
    keyword.forwardUrl = "https://tempuri.org"
    keyword.enabled = True
    keyword.created = "2018-04-12T12:00:00Z"
    keyword.lastModified = "2018-04-15T14:00:00Z"
    keyword.tags = ["Foo", "Bar"]

    # Create a keyword
    createdId = client.CreateKeyword(keyword)

    # Get the created keyword
    fetchedKeyword = client.GetKeyword(str(createdId))
    assert fetchedKeyword.keywordText == keyword.keywordText

    # Update keyword
    fetchedKeyword.keywordText = str(uuid.uuid4())
    client.UpdateKeyword(fetchedKeyword)
    updatedKeyword = client.GetKeyword(str(createdId))
    assert updatedKeyword.keywordText == fetchedKeyword.keywordText

    # Get all with filters returns record
    allKeywords = client.GetAllKeywords(validShortNumberId, None, "Wildcard", "Foo")
    assert len(allKeywords) > 0

    # Delete
    client.DeleteKeyword(str(createdId))

    # Trying to fetch returns None
    assert client.GetKeyword(str(createdId)) is None


def test_OutMessageSequence(client, validShortNumberId):
    tomorrow = _addDays(datetime.utcnow(), 1)
    formatted = _formatDatetime(tomorrow)

    # create
    outMessage = OutMessage()
    outMessage.sender = "0000"
    outMessage.recipient = "+4798079008"
    outMessage.content = "Hi! This is a message from 0000 :)"
    outMessage.sendTime = formatted
    identifier = client.CreateOutMessage(outMessage)

    # get
    fetched = client.GetOutMessage(identifier)
    fetched.content += fetched.content

    # update
    client.UpdateOutMessage(fetched)
    updated = client.GetOutMessage(identifier)
    assert updated.content == fetched.content

    # delete
    client.DeleteOutMessage(identifier)
    assert client.GetOutMessage(identifier) is None

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
    client.CreateOutMessageBatch(messages)

    client.DeleteOutMessage(str(t1))
    client.DeleteOutMessage(str(t2))
    client.DeleteOutMessage(str(t3))

def test_PrepareMsisdns(client):
    client.PrepareMsisdns(["+4798079008"])

def test_LookupShouldReturnResult(client):
    assert client.Lookup("+4798079008") is not None

def test_StrexMerchantIdSequence(client, validShortNumberId):
    merchantIdIdentifier = "12341"

    # create        
    merchantId = StrexMerchantId()
    merchantId.merchantId = merchantIdIdentifier
    merchantId.shortNumberId = validShortNumberId
    merchantId.password = "abcdef"
    client.SaveMerchant(merchantId)

    # get by id
    fetched = client.GetMerchant(merchantIdIdentifier)
    assert fetched is not None

    # get all
    assert len(client.GetMerchantIds()) > 0

    # delete
    client.DeleteMerchant(merchantIdIdentifier)
    assert client.GetMerchant(merchantIdIdentifier) is None


# Formats datetime object into utc string
# got from https://stackoverflow.com/questions/19654578/python-utc-datetime-objects-iso-format-doesnt-include-z-zulu-or-zero-offset
def _formatDatetime(datetime):
    return datetime.strftime('%Y-%m-%dT%H:%M:%S') + datetime.strftime('.%f')[:4] + 'Z'

def _addDays(datetime, daysCount):
    return datetime + timedelta(days=daysCount)
