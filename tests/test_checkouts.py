import decimal
import random
import unittest

from faker import Faker

from paymaya_sdk.sdk import PayMayaSDK
from paymaya_sdk.models.amount_models import AmountModel, TotalAmountModel
from paymaya_sdk.models.buyer_models import BuyerModel
from paymaya_sdk.models.checkout_data_models import CheckoutDataModel
from paymaya_sdk.models.checkout_item_models import CheckoutItemModel

from .merchants import m1

fake = Faker()


class CheckoutTests(unittest.TestCase):
    def test_checkout(self):
        paymaya = PayMayaSDK()
        paymaya.set_keys(
            public_api_key=m1.public_key,
            secret_api_key=m1.secret_key,
            encoded_key="cGstZW80c0wzOTNDV1U1S212ZUpVYVc4VjczMFRUZWkyelk4ekU0ZEhKRHhrRjo="
        )

        checkout = paymaya.checkout()

        amt = 5  # decimal.Decimal(random.uniform(100, 500))
        amount = AmountModel(total=amt, currency_code="PHP")
        single_amount = TotalAmountModel(amount=amount)

        profile = fake.profile()
        buyer = BuyerModel(
            first_name=profile.get("name").split(" ")[0],
            last_name=profile.get("name").split(" ")[-1],
        )
        item = CheckoutItemModel()
        item.name = fake.name()
        item.code = fake.uuid4()
        item.quantity = fake.random_int(1, 10)
        item.amount = single_amount
        total_amount = TotalAmountModel(
            amount=AmountModel(total=item.quantity * amount.total, currency_code="PHP")
        )
        item.total_amount = total_amount

        checkout_data = CheckoutDataModel()
        checkout_data.total_amount = total_amount
        checkout_data.buyer = buyer
        checkout_data.items = [item.as_dict()]
        checkout_data.request_reference_number = fake.uuid4()
        checkout_data.redirect_urls = {
            "success": "https://google.com",
            "failure": "https://yahoo.com",
            "cancel": "https://microsoft.com",
        }

        checkout.initiate(checkout_data)

        result = checkout.execute()

        assert checkout.checkout_data.as_dict().get('redirectUrl').get(
            'success') == 'https://google.com', checkout_data.as_dict()
        """
        Checkout returns:
        - result.json()
        {
            "checkoutId": <UUID>,
            "redirectUrl": <URL>
        }
        """
        assert result, result.json()
