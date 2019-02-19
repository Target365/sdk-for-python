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
* [Lookup](#lookup)
    * [Address lookup for mobile number](#address-lookup-for-mobile-number)
* [Keywords](#keywords)
    * [Create a keyword](#create-a-keyword)
    * [Delete a keyword](#delete-a-keyword)
    * [SMS forward](#sms-forward)
    * [SMS forward using the SDK](#sms-forward-using-the-sdk)

## Introduction
The Target365 SDK gives you direct access to our online services like sending and receiving SMS, address lookup and Strex payment transactions.
The SDK provides an appropriate abstraction level for Python and is officially support by Target365.
The SDK also implements very high security (ECDsaP256 HMAC).

## Setup
### ApiClient
```Python
import pytest
import os
import uuid
import target365_sdk

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

### Create a Strex payment transaction
This example creates a 1 NOK Strex payment transaction that the end user will confirm by replying "OK" to an SMS from Strex.
```Python
transaction = StrexTransaction()
transaction.transactionId = str(uuid.uuid4())
transaction.shortNumber = "2002"
transaction.recipient = "+4798079008"
transaction.merchantId = "YOUR_MERCHANT_ID"
transaction.price = 1
transaction.serviceCode = "14002"
transaction.invoiceText = "Donation test"

target365_client.create_strex_transaction(transaction)
```

### Create a Strex payment transaction with one-time password
This example creates a Strex one-time password sent to the end user and get completes the payment by using the one-time password.
```Python
transaction_id = str(uuid.uuid4())

one_time_password = OneTimePassword()
one_time_password.transactionId = transaction_id
one_time_password.sender = "Target365"
one_time_password.recipient = "+4798079008"
one_time_password.merchantId = "YOUR_MERCHANT_ID"
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
