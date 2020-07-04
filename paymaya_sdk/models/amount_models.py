import json
from decimal import Decimal


class AmountModel:
    total: Decimal
    currency_code: str
    as_float: bool

    def __init__(self, *, total: Decimal = 0.0, currency_code: str = "PHP", as_float: bool = True):
        self.total = round(total, 2)
        self.currency_code = currency_code
        self.as_float = as_float

    def total_as_str(self):
        return str(self.total)

    def total_as_float(self):
        return float(self.total)

    def as_dict(self):
        data = {"currency": self.currency_code}
        if self.as_float:
            data["value"] = self.total_as_float()
        else:
            data["value"] = self.total_as_str()

        return data

    def serialize(self):
        return json.dumps(self.as_dict())


class TotalAmountDetailModel:
    discount: Decimal
    service_charge: Decimal
    shipping_fee: Decimal
    tax: Decimal
    subtotal: Decimal

    def __init__(self):
        self.discount = Decimal(0)
        self.service_charge = Decimal(0)
        self.shipping_fee = Decimal(0)
        self.tax = Decimal(0)
        self.subtotal = Decimal(0)

    def as_dict(self):
        data = {
            "discount": str(self.discount),
            "serviceCharge": str(self.service_charge),
            "shippingFee": str(self.shipping_fee),
            "tax": str(self.tax),
            "subtotal": str(self.subtotal),
        }
        return data

    def serialize(self):
        return json.dumps(self.as_dict())


class TotalAmountModel:
    amount: AmountModel
    details: TotalAmountDetailModel
    as_float: bool

    def __init__(
            self, amount: AmountModel = None, details: TotalAmountDetailModel = None, as_float: bool = True
    ):
        if not amount:
            amount = AmountModel()
        self.amount = amount
        self.details = details
        self.as_float = as_float

    def as_dict(self):
        data = {
            "currency": self.amount.currency_code,
        }
        if self.as_float:
            data["value"] = self.amount.total_as_float()
        else:
            data["value"] = self.amount.total_as_str()

        if self.details:
            data["details"] = self.details.as_dict()
        else:
            data["details"] = {}
        return data

    def serialize(self):
        return json.dumps(self.as_dict())
