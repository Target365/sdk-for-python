import requests
import json
import ecdsa
import binascii
import time
import uuid
import base64
import hashlib
import urllib
import jsonpickle


class HttpClient:
    def __init__(self, baseUri, keyName, privateKey):
        self.keyName = keyName
        self.privateKey = privateKey
        self.baseUri = baseUri
        self.publicKey = ecdsa.SigningKey.from_string(
            binascii.unhexlify(self.privateKey), curve=ecdsa.NIST256p)

    def get(self, path):
        return requests.get(self._build_url(path), headers=self._get_auth_header("get", self._build_url(path)))

    def getWithParams(self, path, queryParams):
        url = self._build_url(path)
        if len(queryParams.keys()) > 0:
            url += "?"

        absoluteUri = (url + urllib.parse.urlencode(queryParams)).lower()
        return requests.get(self._build_url(path), params=queryParams, headers=self._get_auth_header("get", absoluteUri))

    def post(self, path, body):
        jsonEncoded = jsonpickle.encode(body)
        return requests.post(self._build_url(path), data=jsonEncoded, headers=self._get_auth_header("post", self._build_url(path), jsonEncoded))

    def put(self, path, body):
        jsonEncoded = jsonpickle.encode(body)
        return requests.put(self._build_url(path), data=jsonEncoded, headers=self._get_auth_header("put", self._build_url(path), jsonEncoded))

    def delete(self, path):
        return requests.delete(self._build_url(path), headers=self._get_auth_header("delete", self._build_url(path)))

    def _build_url(self, path):
        return (self.baseUri + path).lower()

    def _get_auth_header(self, method, uri, body=None):
        signature = self._get_signature(method, uri, body)
        return {"Authorization": "ECDSA " + signature}

    def _get_signature(self, method, uri, body=None):
        timestamp = int(time.time())
        nounce = uuid.uuid4()

        content_hash = ""
        if body is not None:
            content = body
            signature = hashlib.sha256(content.encode("utf-8")).digest()
            base64_encoded = base64.b64encode(signature)
            content_hash = base64_encoded.decode("utf-8")

        message = method + uri + str(timestamp) + str(nounce) + content_hash
        signature_string = base64.b64encode(self.publicKey.sign(
            message.encode("utf-8"), hashfunc=hashlib.sha256))
        the_signature = self.keyName + ":" + str(timestamp) + ":" + str(nounce) + ":" + signature_string.decode("utf-8")

        return the_signature
