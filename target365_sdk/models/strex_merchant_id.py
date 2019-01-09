from .model import Model

class StrexMerchantId(Model):

    def _accepted_params(self) -> list:
        return [
            'merchantId',
            'shortNumberId',
            'password',
        ]
