from typing import List

from paymaya_sdk.core.api_manager import APIManager
from paymaya_sdk.core.constants import PRODUCTION, DIRECT_PRODUCTION_URL, DIRECT_SANDBOX_URL


class PayMayaDirectAPIManager(APIManager):
    base_url: str = None

    def __init__(self, *args, **kwargs):
        self.base_url = self.get_base_url()
        super().__init__(*args, **kwargs)

    def get_base_url(self) -> str:
        if self.environment == PRODUCTION:
            url = DIRECT_PRODUCTION_URL
        else:
            url = DIRECT_SANDBOX_URL

        return url
