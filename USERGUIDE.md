# Python User Guide

## Table of Contents
* [Introduction](#introduction)
* [Setup](#setup)
    * [ApiClient](#apiclient)
* [Text messages](#text-messages)
    * [Send an SMS](#send-an-sms)
    * [Schedule an SMS for later sending](#schedule-an-sms-for-later-sending)
    * [Edit a scheduled SMS](#edit-a-scheduled-sms)
    * [Delete a scheduled SMS](#delete-a-scheduled-sms)
* [Payment transactions](#payment-transactions)
    * [Create a Strex payment transaction](#create-a-strex-payment-transaction)
    * [Create a Strex payment transaction with one-time password](#create-a-strex-payment-transaction-with-one-time-password)
    * [Reverse a Strex payment transaction](#reverse-a-strex-payment-transaction)
    * [Check status on Strex payment transaction](#check-status-on-strex-payment-transaction)
* [One-click](#one-click)
    * [One-click config](#one-click-config)
    * [Recurring transaction](#recurring-transaction)
* [Lookup](#lookup)
    * [Address lookup for mobile number](#address-lookup-for-mobile-number)
* [Keywords](#keywords)
    * [Create a keyword](#create-a-keyword)
    * [Delete a keyword](#delete-a-keyword)
* [Forwards](#forwards)
    * [SMS forward](#sms-forward)
    * [DLR forward](#dlr-forward)
    * [DLR status codes](#dlr-status-codes)
* [Encoding and SMS length](#encoding-and-sms-length)

## Introduction
The Target365 SDK gives you direct access to our online services like sending and receiving SMS, address lookup and Strex payment transactions.
The SDK provides an appropriate abstraction level for Python and is officially support by Target365.
The SDK also implements very high security (ECDsaP256 HMAC).

Information on how to get the key name and private key is documented in [the README file](README.md).

## Setup
### ApiClient
```Python
import uuid
from target365_sdk import ApiClient

base_url = "https://shared.target365.io"
key_name = "YOUR_KEY"
private_key = "BASE64_EC_PRIVATE_KEY"
target365_client = ApiClient(base_url, key_name, private_key)
```
## Text messages

### Send an SMS
This example sends an SMS to 98079008 (+47 for Norway) from "Target365" with the text "Hello world from SMS!".
```Python
out_message = OutMessage()
out_message.transactionId = str(uuid.uuid4())
out_message.sender = "Target365"
out_message.recipient = "+4798079008"
out_message.content = "Hello World from SMS!"

target365_client.create_out_message(out_message)
```

### Schedule an SMS for later sending
This example sets up a scheduled SMS. Scheduled messages can be updated or deleted before the time of sending.
```Python
send_time = datetime.utcnow() + timedelta(hours=1)

out_message = OutMessage()
out_message.transactionId = str(uuid.uuid4())
out_message.sender = "Target365"
out_message.recipient = "+4798079008"
out_message.content = "Hello World from SMS!"
out_message.sendTime = send_time.strftime('%Y-%m-%dT%H:%M:%S') + send_time.strftime('.%f')[:4] + 'Z'

target365_client.create_out_message(out_message)
```

### Edit a scheduled SMS
This example updates a previously created scheduled SMS.
```Python
out_message = client.get_out_message(transaction_id)
out_message.content = out_message.content + " Extra text :)"

target365_client.update_out_message(out_message)
```

### Delete a scheduled SMS
This example deletes a previously created scheduled SMS.
```Python
target365_client.delete_out_message(transaction_id)
```

## Payment transactions
If your service requires a minimum age of the End User, each payment transaction should be defined with minimum age. Both StrexTransaction and OutMessage have a property named “Age”. If not set or present in the request, there is no age limit.

### Create a Strex payment transaction
This example creates a 1 NOK Strex payment transaction that the end user will confirm by replying "OK" to an SMS from Strex.
You can use message_prefix and message_suffix custom properties to influence the start and end of the SMS sent by Strex.
```Python
transaction = StrexTransaction()
transaction.transactionId = str(uuid.uuid4())
transaction.shortNumber = "2002"
transaction.recipient = "+4798079008"
transaction.merchantId = "YOUR_MERCHANT_ID"
transaction.price = 1
transaction.serviceCode = "14002"
transaction.invoiceText = "Donation test"
transaction.properties = { 'message_prefix': 'Dear customer...', 'message_suffix': 'Best regards...' }
transaction.smsConfirmation = True

target365_client.create_strex_transaction(transaction)
```

### Create a Strex payment transaction with one-time password
This example creates a Strex one-time password sent to the end user and get completes the payment by using the one-time password.
You can use MessagePrefix and MessageSuffix to influence the start and end of the SMS sent by Strex.
```Python
transaction_id = str(uuid.uuid4())

one_time_password = OneTimePassword()
one_time_password.transactionId = transaction_id
one_time_password.sender = "Target365"
one_time_password.recipient = "+4798079008"
one_time_password.merchantId = "YOUR_MERCHANT_ID"
one_time_password.messagePrefix = "Dear customer..."
one_time_password.messageSuffix = "Best regards..."
one_time_password.recurring = False

client.create_one_time_password(one_time_password)

# *** Get input from end user (eg. via web site) ***

transaction = StrexTransaction()
transaction.transactionId = transaction_id
transaction.shortNumber = "2002"
transaction.recipient = "+4798079008"
transaction.merchantId = "YOUR_MERCHANT_ID"
transaction.price = 1
transaction.serviceCode = "14002"
transaction.invoiceText = "Donation test"
transaction.oneTimePassword = "ONE_TIME_PASSWORD_FROM_USER"

target365_client.create_strex_transaction(transaction)
```

### Reverse a Strex payment transaction
This example reverses a previously billed Strex payment transaction. The original transaction will not change, but a reversal transaction will be created that counters the previous transaction by a negative Price.
The reversal transaction id is always the same as the original id prefixed by "-".
```Python
target365_client.delete_strex_transaction(transaction_id)
 
reversal_transaction = target365_client.get_strex_transaction("-" + transaction_id)
```

### Check status on Strex payment transaction
This example gets a previously created Strex transaction to check its status. This method will block up to 20 seconds if the transaction is still being processed.
```Python
transaction = target365_client.get_strex_transaction(transaction_id);
statusCode = transaction.statusCode;
```

## One-click

Please note:

* The OneClick service will not stop same MSISDN to order several times as long as transactionID is unique. If end users order or subscribe several times to same service it's the merchants responsibility to refund the end user.

* Recurring billing is initiated by merchants, see section [Payment transactions](#payment-transactions) for more info.

* Since the one-click flow ends by redirecting the end user to an external merchant-controlled URL we recommend that merchants implement a mechanism to check status on all started transactions. If there’s any issue for the end user on their way to the last page they might have finished the payment, but not been able to get their product.

### One-click config
This example sets up a one-click config which makes it easier to handle campaigns in one-click where most properties like merchantId, price et cetera are known in advance. You can redirect the end-user to the one-click campaign page by redirecting to http://betal.strex.no/{YOUR-CONFIG-ID} for PROD and http://test-strex.target365.io/{YOUR-CONFIG-ID} for TEST-environment. You can also set the TransactionId by adding ?id={YOUR-TRANSACTION-ID} to the URL.

```Python
config_data = OneClickConfig()
config.configId = "YOUR_CONFIG_ID"
config.shortNumber = "2002"
config.price = 99
config.merchantId = "YOUR_MERCHANT_ID"
config.businessModel = "STREX-PAYMENT"
config.serviceCode = "14002"
config.invoiceText = "Donation test"
config.onlineText = "Buy directly"
config.offlineText = "Buy with PIN-code"
config.redirectUrl = "https://your-return-url.com?id={TransactionId}" # Placeholder {TransactionId} is replaced by actual id
config.subscriptionPrice = 99
config.subscriptionInterval = "monthly"
config.subscriptionStartSms = "Thanks for donating 99kr each month."
config.recurring = False
config.isRestricted = False
config.age = 0

target365_client.save_oneclick_config(config)
```

If Recurring is set to 'false', the following parameters are optional:

* SubscriptionInterval - Possible values are "weekly", "monthly", "yearly"

* SubscriptionPrice - How much the subscriber will be charged each interval

This parameter is optional:

* SubscriptionStartSms - SMS that will be sent to the user when subscription starts.

### Recurring transaction
This example sets up a recurring transaction for one-click. After creation you can immediately get the transaction to get the status code - the server will wait up to 20 seconds for the async transaction to complete.
![Recurring sequence](https://github.com/Target365/sdk-for-python/raw/master/oneclick-recurring-flow.png "Recurring sequence diagram")
```Python
transaction = StrexTransaction()
transaction.transactionId = transaction_id
transaction.recipient = 'RECIPIENT_FROM_SUBSCRIPTION'
transaction.shortNumber = "2002"
transaction.merchantId = "YOUR_MERCHANT_ID"
transaction.price = 1
transaction.serviceCode = "14002"
transaction.invoiceText = "Donation test"

target365_client.create_strex_transaction(transaction)
transaction = target365_client.get_strex_transaction(transaction_id)

# *** TODO: Check transaction statusCode ***
```

## Lookup

### Address lookup for mobile number
This example looks up address information for the mobile number 98079008. Lookup information includes registered name and address.
```Python
lookup = target365_client.lookup("+4798079008")
first_name = lookup.firstName
last_name = lookup.lastName
```

## Keywords

### Create a keyword
This example creates a new keyword on short number 2002 that forwards incoming SMS messages to 2002 that starts with "HELLO" to the URL  "https://your-site.net/api/receive-sms".
```Python

keyword = Keyword()
keyword.shortNumberId = "NO-2002"
keyword.keywordText = "HELLO"
keyword.mode = "Text"
keyword.forwardUrl = "https://your-site.net/api/receive-sms"
keyword.enabled = True

keyword_id = target365_client.create_keyword(keyword)
```

### Delete a keyword
This example deletes a keyword.
```Python
target365_client.delete_keyword(keyword_id)
```
## Forwards

### SMS forward
This example shows how SMS messages are forwarded to the keywords ForwardUrl. All sms forwards expects a response with status code 200 (OK). If the request times out or response status code differs the forward will be retried several times.
#### Request
```
POST https://your-site.net/api/receive-sms HTTP/1.1
Content-Type: application/json
Host: your-site.net

{
  "transactionId":"00568c6b-7baf-4869-b083-d22afc163059",
  "created":"2019-02-07T21:11:00+00:00",
  "sender":"+4798079008",
  "recipient":"2002",
  "content":"HELLO"
}
```

#### Response
```
HTTP/1.1 200 OK
Date: Thu, 07 Feb 2019 21:13:51 GMT
Content-Length: 0
```

### DLR forward
This example shows how delivery reports (DLR) are forwarded to the outmessage DeliveryReportUrl. All DLR forwards expect a response with status code 200 (OK). If the request times out or response status code differs the forward will be retried 10 times with exponentially longer intervals for about 15 hours.
#### Request
```
POST https://your-site.net/api/receive-dlr HTTP/1.1
Content-Type: application/json
Host: your-site.net

{
    "correlationId": null,
    "transactionId": "client-specified-id-5c88e736bb4b8",
    "price": null,
    "sender": "Target365",
    "recipient": "+4798079008",
    "operatorId": "no.telenor",
    "statusCode": "Ok",
    "detailedStatusCode": "Delivered",
    "delivered": true,
    "billed": null,
    "smscTransactionId": "16976c7448d",
    "smscMessageParts": 1
}
```

#### Response
```
HTTP/1.1 200 OK
Date: Thu, 07 Feb 2019 21:13:51 GMT
Content-Length: 0
```

### DLR status codes
Delivery reports contains two status codes, one overall called `StatusCode` and one detailed called `DetailedStatusCode`.

#### StatusCode values
|Value|Description|
|:---|:---|
|Queued|Message is queued|
|Sent|Message has been sent|
|Failed|Message has failed|
|Ok|message has been delivered/billed|
|Reversed|Message billing has been reversed|

#### DetailedStatusCode values
|Value|Description|
|:---|:---|
|None|Message has no status|
|Delivered|Message is delivered to destination|
|Expired|Message validity period has expired|
|Undelivered|Message is undeliverable|
|UnknownError|Unknown error|
|Rejected|Message has been rejected|
|UnknownSubscriber|Unknown subscriber|
|SubscriberUnavailable|Subscriber unavailable|
|SubscriberBarred|Subscriber barred|
|InsufficientFunds|Insufficient funds|
|RegistrationRequired|Registration required|
|UnknownAge|Unknown age|
|DuplicateTransaction|Duplicate transaction|
|SubscriberLimitExceeded|Subscriber limit exceeded|
|MaxPinRetry|Max pin retry reached|
|InvalidAmount|Invalid amount|
|OneTimePasswordExpired|One-time password expired|
|OneTimePasswordFailed|One-time password failed|
|SubscriberTooYoung|Subscriber too young|
|TimeoutError|Timeout error|

## Encoding and SMS length
When sending SMS messages, we'll automatically send messages in the most compact encoding possible. If you include any non GSM-7 characters in your message body, we will automatically fall back to UCS-2 encoding (which will limit message bodies to 70 characters each).

Additionally, for long messages--greater than 160 GSM-7 characters or 70 UCS-2 characters--we will split the message into multiple segments. Six (6) bytes is also needed to instruct receiving device how to re-assemble messages, which for multi-segment messages, leaves 153 GSM-7 characters or 67 UCS-2 characters per segment.

Note that this may cause more message segments to be sent than you expect - a body with 152 GSM-7-compatible characters and a single unicode character will be split into three (3) messages because the unicode character changes the encoding into less-compact UCS-2. This will incur charges for three outgoing messages against your account.

Norwegian operators support different numbers of segments; Ice 12 segments, Telia 20 segments and Telenor 255 segments.
