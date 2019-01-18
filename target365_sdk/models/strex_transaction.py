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
            'content',
            'serviceCode',
            'created',
            'deliveryMode',
            'statusCode',
            'accountId',
            'billed',
        ]
