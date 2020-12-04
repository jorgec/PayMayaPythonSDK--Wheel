import decimal
import random
import unittest

from faker import Faker

from paymaya_sdk.models.amount_models import AmountModel
from paymaya_sdk.models.buyer_models import BuyerModel
from paymaya_sdk.sdk import PayMayaSDK
from .wallets import w1, w2, wu

fake = Faker()


class WalletTests(unittest.TestCase):
    def test_wallet_single_payment(self):
        paymaya = PayMayaSDK()
        paymaya.set_keys(
            public_api_key=w2.public_key,
            secret_api_key=w2.secret_key
        )

        dp = paymaya.direct_payment()
        amt = decimal.Decimal(random.uniform(100, 10000))
        amount = AmountModel(total=amt, currency_code="PHP")
        dp.amount = amount
        dp.request_ref = "testlocal"
        dp.redirect_urls = {
            "success": "http://success.com",
            "failure": "http://failure.com",
            "cancel": "http://cancel.com",
        }
        payment_result = dp.execute_single_payment()

        assert payment_result.status_code == 201, print(payment_result.json(), dp.last_transaction)
