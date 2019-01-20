from .model import Model

class StrexTransaction(Model):

    def _accepted_params(self):
        return [
            'transactionId',
            'invoiceText',
            'lastModified',
            'merchantId',
            'price',
            'shortNumber',
            'recipient',
            'oneTimePassword',
            'content',
            'serviceCode',
            'created',
            'deliveryMode',
            'statusCode',
            'accountId',
            'billed',
            'properties',
            'tags',

            'strexOtpTransactionId',  # TODO the API is going to be changed to stop returning this property
            'smscTransactionId',  # TODO the API is going to be changed to stop returning this property
            'eTag',  # TODO the API is going to be changed to stop returning this property
        ]
