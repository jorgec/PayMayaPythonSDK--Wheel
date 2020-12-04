import json
from typing import Dict

import requests

from paymaya_sdk.core.constants import (
    REDIRECT_URLS, DIRECT_SINGLE_PAYMENT
)
from paymaya_sdk.core.http_config import HTTP_PUT, HTTP_DELETE
from paymaya_sdk.core.paymaya_direct_api_manager import PayMayaDirectAPIManager
from paymaya_sdk.models.amount_models import AmountModel
from paymaya_sdk.models.direct_payment_model import DirectPaymentModel


class PaymayaDirectAPI:
    amount: AmountModel = None
    request_ref: str = None
    redirect_urls: Dict = {}
    metadata: Dict = {}

    last_transaction: Dict = None

    manager: PayMayaDirectAPIManager

    def __init__(self, *args, **kwargs):
        self.public_api_key = kwargs.get("public_api_key")
        self.secret_api_key = kwargs.get("secret_api_key")
        self.environment = kwargs.get("environment")
        self.init_manager()

    def init_manager(self):
        manager_data = {
            "public_api_key": self.public_api_key,
            "secret_api_key": self.secret_api_key,
            "environment": self.environment,
        }

        self.manager = PayMayaDirectAPIManager(**manager_data)

    def pre_payment_checks(self):
        if not self.amount:
            raise AttributeError("No amount")

        if not self.request_ref:
            raise AttributeError("No request reference set")

        if not self.redirect_urls:
            self.redirect_urls = REDIRECT_URLS

    def execute_single_payment(self) -> requests.Response:
        self.pre_payment_checks()

        url = f"{self.manager.get_base_url()}{DIRECT_SINGLE_PAYMENT}"
        payment_data = {"amount": self.amount, "urls": self.redirect_urls, "request_ref": self.request_ref}

        if self.metadata:
            payment_data["metadata"] = self.metadata

        payment = DirectPaymentModel(**payment_data)

        self.last_transaction = {
            "url": url,
            "payload": payment.as_dict(),
            "headers": self.manager.http_headers
        }

        result = self.manager.execute(
            url=url,
            payload=payment.serialize(),
            key="public"
        )
        return result
