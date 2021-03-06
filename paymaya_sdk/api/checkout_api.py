import json
from typing import Dict

import requests

from paymaya_sdk.core.checkout_api_manager import CheckoutAPIManager
from paymaya_sdk.core.constants import CHECKOUTS_URL, WEBHOOKS_URL, CUSTOMIZATIONS_URL, REDIRECT_URLS
from paymaya_sdk.core.http_config import HTTP_PUT, HTTP_DELETE, HTTP_POST
from paymaya_sdk.models.checkout_customization_models import CheckoutCustomizationModel
from paymaya_sdk.models.checkout_data_models import CheckoutDataModel


class CheckoutAPI:
    checkout_data: CheckoutDataModel

    public_api_key: str = None
    secret_api_key: str = None
    environment: str = "SANDBOX"
    encoded_key: str = None
    last_url: str = None
    redirect_urls: Dict = None
    request_reference_number: str = None

    manager: CheckoutAPIManager

    def __init__(self, *args, **kwargs):
        self.public_api_key = kwargs.get("public_api_key")
        self.secret_api_key = kwargs.get("secret_api_key")
        self.environment = kwargs.get("environment")
        self.encoded_key = kwargs.get("encoded_key", None)
        self.init_manager()

    def init_manager(self):
        manager_data = {
            "public_api_key": self.public_api_key,
            "secret_api_key": self.secret_api_key,
            "environment": self.environment,
        }
        if self.encoded_key:
            manager_data["encoded_key"] = self.encoded_key
        self.manager = CheckoutAPIManager(**manager_data)

    def initiate(self, checkout_data: CheckoutDataModel) -> None:
        """
        Placeholder method in case we need to do some more pre-processing later
        :param checkout_data:
        :return:
        """

        self.checkout_data = checkout_data

    def execute(self, key: str = "secret", method: str = HTTP_POST) -> requests.Response:
        if not self.checkout_data:
            raise ValueError("No Checkout Data")

        url = f"{self.manager.get_base_url()}{CHECKOUTS_URL}"
        self.last_url = url

        if self.request_reference_number:
            self.checkout_data['requestReferenceNumber'] = self.request_reference_number

        return self.manager.execute(url=url, payload=self.checkout_data.serialize(), key=key, method=method)

    # The Webhooks API seems to be borked ¯\_(ツ)_/¯
    # TODO: Tests

    def register_webhook(self, name: str, callback_url: str) -> requests.Response:
        payload = json.dumps({"name": name, "callbackUrl": callback_url})
        url = f"{self.manager.get_base_url()}{WEBHOOKS_URL}"

        return self.manager.execute(url=url, payload=payload)

    def get_webhooks(self) -> requests.Response:
        url = f"{self.manager.get_base_url()}{WEBHOOKS_URL}"
        return self.manager.query(url=url)

    def update_webhook(self, webhook_id: str, fields: Dict) -> requests.Response:
        url = f"{self.manager.get_base_url()}{WEBHOOKS_URL}/{webhook_id}"
        payload = json.dumps(fields)
        return self.manager.execute(url=url, payload=payload, method=HTTP_PUT)

    def delete_webhook(self, webhook_id: str):
        url = f"{self.manager.get_base_url()}{WEBHOOKS_URL}/{webhook_id}"
        return self.manager.execute(url=url, method=HTTP_DELETE)

    def register_customization(self, customization: CheckoutCustomizationModel):
        url = f"{self.manager.get_base_url()}{CUSTOMIZATIONS_URL}"
        payload = customization.serialize()
        return self.manager.execute(url=url, payload=payload)

    def get_customizations(self):
        url = f"{self.manager.get_base_url()}{CUSTOMIZATIONS_URL}"
        return self.manager.query(url=url)

    def delete_customizations(self):
        url = f"{self.manager.get_base_url()}{CUSTOMIZATIONS_URL}"
        return self.manager.execute(url=url, method=HTTP_DELETE)
