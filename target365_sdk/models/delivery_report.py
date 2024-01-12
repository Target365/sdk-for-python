from .model import Model

class DeliveryReport(Model):

    def _accepted_params(self):
        return [
              'correlationId',
              'sessionId',
              'transactionId',
              'price',
              'sender',
              'recipient',
              'operatorId',
              'statusCode',
              'detailedStatusCode',
              'statusDescription',
              'delivered',
              'billed',
              'smscTransactionId',
              'smscMessageParts',
              'smscStatus',
              'received',
              'properties',
        ]
