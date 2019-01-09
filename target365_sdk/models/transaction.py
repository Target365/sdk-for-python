from .model import Model

class Transaction(Model):

    def _accepted_params(self) -> list:
        return [
            'transactionId',
            'invoiceText',
            'lastModified',
            'merchantId',
            'price',
            'recipient',
            'serviceCode',
            'shortNumber',
            'created',

            'deliveryMode',
            'statusCode',
            'accountId',
            'strexOtpTransactionId',
            'smscTransactionId',
            'eTag',
            'billed',
        ]

