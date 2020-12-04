from paymaya_sdk.models.user_account_models import PaymayaUserAccountModel


class Wallet:
    name: str
    is_pf: bool

    secret_key: str
    public_key: str

    def __init__(self, name: str, secret: str, public: str, is_pf: bool = True):
        self.name = name
        self.secret_key = secret
        self.public_key = public
        self.is_pf = is_pf


w1 = Wallet(
    "Payment Facilitator",
    "sk-6s9dwnYGFJdZOYu1HCUAfUZctWEf9AjtHIG38kezX8W",
    "pk-rpwb5YR6EfnKiMsldZqY4hgpvJjuy8hhxW2bVAAiz2N"
)

w2 = Wallet(
    "Non-Payment Facilitator",
    "sk-NMda607FeZNGRt9xCdsIRiZ4Lqu6LT898ItHbN4qPSe",
    "pk-MOfNKu3FmHMVHtjyjG7vhr7vFevRkWxmxYL1Yq6iFk5",
    is_pf=False
)

wu = PaymayaUserAccountModel(
    "09193890579",
    "Password123"
)
