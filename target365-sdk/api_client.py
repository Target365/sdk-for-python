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
    IN_MESSAGES = "api/in-messages"
    PREPARE_MSISDNS = "api/prepare-msisdns"
    STREX_MERCHANTS = "api/strex/merchants"
    STREX_TRANSACTIONS = "api/strex/transactions"
    STREX_ONE_TIME_PASSWORDS = "api/strex/one-time-passwords"
    SERVER_PUBLIC_KEYS = "api/server/public-keys"
    CLIENT_PUBLIC_KEYS = "api/client/public-keys"

    NOT_FOUND = 404

    def __init__(self, base_uri, key_name, private_key):
        self.client = HttpClient(base_uri, key_name, private_key)
        self.errorHandler = HttpErrorHandler()

    ###  Ping controller  ###

    def ping(self):
        """
        GET /api/ping
        Pings the service and returns a hello message
        :return: return description
        """
        response = self.client.get(self.PING)
        self.errorHandler.throw_if_not_success(response)
        return response.text # returns the string "pong"

    ###  Lookup controller  ###

    def loopup(self, msisdn):
        """
        GET /api/lookup
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
        self.errorHandler.throw_if_not_success(response)
        lookupResult = LookupResult()
        lookupResult.from_dict(response.json())
        return lookupResult

    ###  Keyword controller  ###

    def create_keyword(self, keyword):
        """
        POST /api/keywords
        Creates a new keyword.
        :keyword: Keyword
        :return: string
        """
        if keyword is None:
            raise ValueError("keyword")
        response = self.client.post(self.KEYWORDS, keyword)
        self.errorHandler.throw_if_not_success(response)

        return self._get_id_from_header(response.headers)

    def get_all_keywords(self, short_number_id=None, keyword=None, mode=None, tag=None):
        """
        GET /api/keywords
        Gets all keywords.
        :return: Keyword[]
        """
        params = {}
        if short_number_id is not None:
            params["shortNumberId"] = short_number_id
        if keyword is not None:
            params["keywordText"] = keyword
        if mode is not None:
            params["mode"] = mode
        if tag is not None:
            params["tag"] = tag

        response = self.client.getWithParams(self.KEYWORDS, params)
        self.errorHandler.throw_if_not_success(response)
        return Keyword().from_response_list(response.json())

    def get_keyword(self, keyword_id):
        """
        GET /api/keywords/{keywordId}
        Gets a keyword.
        :keywordId: string
        :return: Keyword
        """
        if keyword_id is None:
            raise ValueError("keywordId")

        response = self.client.get(self.KEYWORDS + "/" + keyword_id)
        if response.status_code == self.NOT_FOUND:
            return None

        self.errorHandler.throw_if_not_success(response)
        
        keyword = Keyword()
        keyword.from_dict(response.json())
        return keyword

    def update_keyword(self, keyword):
        """
        PUT /api/keywords/{keywordId}
        Updates a keyword
        :keyword: Keyword to update      
        """
        if keyword is None:
            raise ValueError("keyword")
        if keyword.keywordId is None:
            raise ValueError("keywordId")

        response = self.client.put(
            self.KEYWORDS + "/" + keyword.keywordId, keyword)

        self.errorHandler.throw_if_not_success(response)

    def delete_keyword(self, keyword_id):
        """
        DELETE /api/keywords/{keywordId}
        Deletes a keyword
        :keywordId: string
        """
        if keyword_id is None:
            raise ValueError("keywordId")

        response = self.client.delete(self.KEYWORDS + "/" + keyword_id)
        self.errorHandler.throw_if_not_success(response)

    ###  OutMessage controller  ###

    def prepare_msisdns(self, msisdns):
        """
        POST /api/prepare-msisdns
        MSISDNs to prepare as a string array
        :message: string[]
        """
        if msisdns is None:
            raise ValueError("msisdns")
        response = self.client.post(self.PREPARE_MSISDNS, msisdns)
        self.errorHandler.throw_if_not_success(response)

    def create_out_message(self, message):
        """
        POST /api/out-messages
        Creates a new out-message
        :message: OutMessage
        """
        if message is None:
            raise ValueError("message")

        response = self.client.post(self.OUT_MESSAGES, message)
        self.errorHandler.throw_if_not_success(response)

        return self._get_id_from_header(response.headers)

    def create_out_message_batch(self, messages):
        """
        POST /api/out-messages/batch
        Creates a new out-message batch.
        :messages: OutMessage[]
        """
        if messages is None:
            raise ValueError("messages")

        response = self.client.post(self.OUT_MESSAGES + "/batch", messages)
        self.errorHandler.throw_if_not_success(response)

    def get_out_message(self, transaction_id):
        """
        GET /api/out-messages/batch/{transactionId}
        Gets and out-message
        :transactionId: string
        :return: OutMessage
        """
        if transaction_id is None:
            raise ValueError("transactionId")

        response = self.client.get(self.OUT_MESSAGES + "/" + transaction_id)
        if response.status_code == self.NOT_FOUND:
            return None

        self.errorHandler.throw_if_not_success(response)
        outMessage = OutMessage()
        outMessage.from_dict(response.json())
        return outMessage


    def update_out_message(self, message):
        """
        PUT /api/out-messages/batch/{transactionId}
        Updates a future scheduled out-message.
        :message: OutMessage
        """
        if message is None:
            raise ValueError("message")
        if message.transactionId is None:
            raise ValueError("transactionId")

        response = self.client.put(
            self.OUT_MESSAGES + "/" + message.transactionId, message)
        self.errorHandler.throw_if_not_success(response)


    def delete_out_message(self, transaction_id):
        """
        DELETE /api/out-messages/batch/{transactionId}
        Deletes a future sheduled out-message.
        :transactionId: string
        """
        if transaction_id is None:
            raise ValueError("transactionId")

        response = self.client.delete(self.OUT_MESSAGES + "/" + transaction_id)
        self.errorHandler.throw_if_not_success(response)


    ###  InMessages controller  ###

    def get_in_message(self, shortNumberId, transaction_id):
        """
        GET /api/in-messages/{shortNumberId}/{transactionId}
        Gets and in-message
        :shortNumberId: string
        :transactionId: string
        :return: Dict
        """
        if transaction_id is None:
            raise ValueError("transactionId")

        response = self.client.get(self.IN_MESSAGES + "/" + shortNumberId + "/" + transaction_id)
        self.errorHandler.throw_if_not_success(response)

        return response.json()


    ###  StrexMerchantIds controller  ###

    def get_merchant_ids(self):
        """
        GET /api/strex/merchants
        Gets all merchant ids.
        :return: StrexMerchantId[]
        """
        response = self.client.get(self.STREX_MERCHANTS)
        self.errorHandler.throw_if_not_success(response)
        return StrexMerchantId().from_response_list(response.json())

    def get_merchant(self, merchant_id):
        """
        GET /api/strex/merchants/{merchantId}
        Gets a merchant.
        :merchantId: string
        :returns: StrexMerchantId
        """
        if merchant_id is None:
            raise ValueError("merchantId")

        response = self.client.get(self.STREX_MERCHANTS + "/" + merchant_id)

        if response.status_code == self.NOT_FOUND:
            return None

        self.errorHandler.throw_if_not_success(response)
        strexMerchantId = StrexMerchantId()
        strexMerchantId.from_dict(response.json())
        return strexMerchantId

    def save_merchant(self, merchant):
        """
        PUT /api/strex/merchants/{merchantId}
        Creates/updates a merchant.
        :merchant: StrexMerchantId
        """
        if merchant is None:
            raise ValueError("merchant")
        if merchant.merchantId is None:
            raise ValueError("merchantId")

        response = self.client.put(self.STREX_MERCHANTS + "/" + merchant.merchantId, merchant)
        self.errorHandler.throw_if_not_success(response) # expecting http 204 response (no content)

    def delete_merchant(self, merchantId):
        """
        DELETE /api/strex/merchants/{merchantId}
        Deletes a merchant
        :merchantId: string
        """
        if merchantId is None:
            raise ValueError("merchantId")

        response = self.client.delete(self.STREX_MERCHANTS + "/" + merchantId)
        self.errorHandler.throw_if_not_success(response)


    def create_one_time_password(self, oneTimePasswordData):
        """
        POST /api/strex/one-time-passwords
        :return:
        """

        if oneTimePasswordData is None:
            raise ValueError("invalid oneTimePasswordData")
        if oneTimePasswordData['transactionId'] is None:
            raise ValueError("invalid oneTimePasswordData.transactionId")
        if oneTimePasswordData['merchantId'] is None:
            raise ValueError("invalid oneTimePasswordData.merchantId")
        if oneTimePasswordData['recipient'] is None:
            raise ValueError("invalid oneTimePasswordData.recipient")
        if oneTimePasswordData['sender'] is None:
            raise ValueError("invalid oneTimePasswordData.sender")
        if oneTimePasswordData['recurring'] is None:
            raise ValueError("invalid oneTimePasswordData.recurring")

        response = self.client.post(self.STREX_ONE_TIME_PASSWORDS, oneTimePasswordData)
        self.errorHandler.throw_if_not_success(response)


    def get_one_time_password(self, transactionId):
        """
        GET /api/strex/one-time-passwords/{transactionId}

        :param transactionId:
        :return: OneTimePasswordInfo
        """

        response = self.client.get(self.STREX_ONE_TIME_PASSWORDS + '/' + transactionId)
        self.errorHandler.throw_if_not_success(response)

        return response.json()


    def create_transaction(self, transactionData):
        """
        POST /api/strex/transactions
        :return:
        """

        response = self.client.post(self.STREX_TRANSACTIONS, transactionData)
        self.errorHandler.throw_if_not_success(response)

        return self._get_id_from_header(response.headers)


    def get_transaction(self, transactionId):
        """
        GET /api/strex/transactions/{transactionId}
        :return:
        """

        response = self.client.get(self.STREX_TRANSACTIONS + '/' + transactionId)
        self.errorHandler.throw_if_not_success(response)

        return response.json()


    def delete_transaction(self, transactionId):
        """
        DELETE /api/strex/transactions/{transactionId}
        :param transactionId:
        :return:
        """
        response = self.client.delete(self.STREX_TRANSACTIONS + '/' + transactionId)
        self.errorHandler.throw_if_not_success(response)


    ### PublicKey controller  ###

    def get_server_public_key(self, keyName):
        """
        GET /api/server/public-keys/{keyName}
        :param keyName:
        :return:
        """
        response = self.client.get(self.SERVER_PUBLIC_KEYS + '/' + keyName)
        self.errorHandler.throw_if_not_success(response)

        return response.json()


    def get_client_public_keys(self):
        """
        GET /api/client/public-keys
        :return: List
        """
        response = self.client.get(self.CLIENT_PUBLIC_KEYS)
        self.errorHandler.throw_if_not_success(response)

        return response.json()


    def get_client_public_key(self, keyName):
        """
        GET /api/client/public-keys/{keyName}
        :return: Dict
        """
        response = self.client.get(self.CLIENT_PUBLIC_KEYS + '/' + keyName)
        self.errorHandler.throw_if_not_success(response)

        return response.json()


    def delete_client_public_key(self, keyName):
        """
        DELETE /api/client/public-keys/{keyName}
        :return:
        """
        response = self.client.delete(self.CLIENT_PUBLIC_KEYS + '/' + keyName)
        self.errorHandler.throw_if_not_success(response)


    def _get_id_from_header(self, headers):
        """
        Returns the newly created resource's identifier from the Locaion header
        :returns: resource identifier
        """
        chunks = headers["Location"].split("/")
        return chunks[-1]

