import pytest
import os
import uuid
from datetime import datetime
from datetime import timedelta
from api_client import ApiClient
from models.keyword import Keyword
from models.out_message import OutMessage
from models.strex_merchant_id import StrexMerchantId

@pytest.fixture
def valid_short_number_id():
    return 'NO-0000'

@pytest.fixture
def transaction_id():
    return '79f35793-6d70-423c-a7f7-ae9fb1024f3b'


@pytest.fixture(scope="session")
def random_transaction_id():
    return str(uuid.uuid4())

@pytest.fixture
def api_key_name():
    return os.environ['API_KEY_NAME']

@pytest.fixture
def api_private_key():
    return os.environ['API_PRIVATE_KEY']

@pytest.fixture
def client(api_key_name, api_private_key):
    baseUri = "https://test.target365.io/"

    client = ApiClient(baseUri, api_key_name, api_private_key)

    return client


def test_keyword_sequence(client, valid_short_number_id):
    keyword = Keyword()
    keyword.shortNumberId = valid_short_number_id
    keyword.keywordText = str(uuid.uuid4())
    keyword.mode = "Wildcard"
    keyword.forwardUrl = "https://tempuri.org"
    keyword.enabled = True
    keyword.created = "2018-04-12T12:00:00Z"
    keyword.lastModified = "2018-04-15T14:00:00Z"
    keyword.tags = ["Foo", "Bar"]

    # Create a keyword
    createdId = client.create_keyword(keyword)

    # Get the created keyword
    fetchedKeyword = client.get_keyword(str(createdId))
    assert fetchedKeyword.keywordText == keyword.keywordText

    # Update keyword
    fetchedKeyword.keywordText = str(uuid.uuid4())
    client.update_keyword(fetchedKeyword)
    updatedKeyword = client.get_keyword(str(createdId))
    assert updatedKeyword.keywordText == fetchedKeyword.keywordText

    # Get all with filters returns record
    allKeywords = client.get_all_keywords(valid_short_number_id, None, "Wildcard", "Foo")
    assert len(allKeywords) > 0

    # Delete
    client.delete_keyword(str(createdId))

    # Trying to fetch returns None
    assert client.get_keyword(str(createdId)) is None


def test_out_message_sequence(client, valid_short_number_id):
    tomorrow = _add_days(datetime.utcnow(), 1)
    formatted = _format_datetime(tomorrow)

    # create
    outMessage = OutMessage()
    outMessage.sender = "0000"
    outMessage.recipient = "+4798079008"
    outMessage.content = "Hi! This is a message from 0000 :)"
    outMessage.sendTime = formatted
    identifier = client.create_out_message(outMessage)

    # get
    fetched = client.get_out_message(identifier)
    fetched.content += fetched.content

    # update
    client.update_out_message(fetched)
    updated = client.get_out_message(identifier)
    assert updated.content == fetched.content

    # delete
    client.delete_out_message(identifier)
    assert client.get_out_message(identifier) is None

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
    client.create_out_message_batch(messages)

    client.delete_out_message(str(t1))
    client.delete_out_message(str(t2))
    client.delete_out_message(str(t3))

def test_prepare_msisdns(client):
    client.prepare_msisdns(["+4798079008"])


def test_get_in_message(client, valid_short_number_id, transaction_id ):
    in_message_info = client.get_in_message(valid_short_number_id, transaction_id)
    assert in_message_info['transactionId'] == transaction_id


def test_lookup_should_return_result(client):
    assert client.loopup("+4798079008") is not None


def test_strex_merchant_id_sequence(client, valid_short_number_id):
    merchantIdIdentifier = "12341"

    # create        
    merchantId = StrexMerchantId()
    merchantId.merchantId = merchantIdIdentifier
    merchantId.shortNumberId = valid_short_number_id
    merchantId.password = "abcdef"
    client.save_merchant(merchantId)

    # get by id
    fetched = client.get_merchant(merchantIdIdentifier)
    assert fetched is not None

    # get all
    assert len(client.get_merchant_ids()) > 0

    # delete
    client.delete_merchant(merchantIdIdentifier)
    assert client.get_merchant(merchantIdIdentifier) is None


def test_create_one_time_password(client, random_transaction_id):

    oneTimePasswordData = {
        'transactionId': random_transaction_id,
        'merchantId': 'mer_test',
        'recipient': '+4798079008',
        'sender': 'Test',
        'recurring': False
    }

    client.create_one_time_password(oneTimePasswordData)


def test_get_time_password(client, transaction_id):
    oneTimePasswordInfo = client.get_one_time_password(transaction_id)

    assert oneTimePasswordInfo['transactionId'] == transaction_id


def test_transaction_sequence(client, random_transaction_id):
    transactionData = {
        "created": "2018-11-02T12:00:00Z",
        "invoiceText": "Thank you for your donation",
        "lastModified": "2018-11-02T12:00:00Z",
        "merchantId": "mer_test",
        "price": 10,
        "recipient": "+4798079008",
        "serviceCode": "14002",
        "shortNumber": "2001",
        "transactionId": random_transaction_id
    }

    client.create_transaction(transactionData)

    transactionData = client.get_transaction(random_transaction_id)
    assert transactionData['transactionId'] == random_transaction_id

    client.delete_transaction(random_transaction_id)


def test_get_server_public_key(client):
    responseData = client.get_server_public_key('2017-11-17')

    assert responseData['accountId'] == 8


def test_get_client_public_keys(client, api_key_name):
    client_public_keys = client.get_client_public_keys()

    found_key = False
    for client_public_key in client_public_keys:
        if client_public_key['name'] == api_key_name:
            found_key = True

    assert found_key == True


def test_get_client_public_key(client, api_key_name):
    client_public_key = client.get_client_public_key(api_key_name)

    assert client_public_key['name'] == api_key_name


# Formats datetime object into utc string
# got from https://stackoverflow.com/questions/19654578/python-utc-datetime-objects-iso-format-doesnt-include-z-zulu-or-zero-offset
def _format_datetime(datetime):
    return datetime.strftime('%Y-%m-%dT%H:%M:%S') + datetime.strftime('.%f')[:4] + 'Z'

def _add_days(datetime, daysCount):
    return datetime + timedelta(days=daysCount)
