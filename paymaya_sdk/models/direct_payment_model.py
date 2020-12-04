import json
from typing import Dict

from paymaya_sdk.core.constants import REDIRECT_URLS
from paymaya_sdk.models.amount_models import AmountModel


class DirectPaymentModel:
    amount: AmountModel
    redirect_urls: Dict
    request_ref: str
    metadata: Dict

    def __init__(
            self,
            *,
            amount: AmountModel,
            request_ref: str,
            urls: Dict = REDIRECT_URLS,
            metadata: Dict = None
    ):
        self.amount = amount
        self.request_ref = request_ref
        self.metadata = metadata
        self.redirect_urls = urls

    def as_dict(self):
        data = {
            "totalAmount": self.amount.as_dict(),
            "redirectUrl": self.redirect_urls,
            "requestReferenceNumber": self.request_ref,
            "metadata": self.metadata
        }

        return data

    def serialize(self):
        return json.dumps(self.as_dict())
