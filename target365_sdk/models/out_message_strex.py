from .model import Model

class OutMessageStrex(Model):


    def _accepted_params(self):
        return [
            'merchantId',
            'serviceCode',
            'businessModel',
            'age',
            'isRestricted',
            'smsConfirmation',
            'invoiceText',
            'price',
            'billed',
            'resultCode',
            'resultDescription',
        ]
