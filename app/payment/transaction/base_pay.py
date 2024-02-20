from abc import ABC, abstractmethod


class Transaction(ABC):
    def __init__(self) -> None:
        self.config = self.get_config()

    @abstractmethod
    def get_config(self):
        pass

    @abstractmethod
    def get_base_url(self, sandbox_mode):
        pass

    @abstractmethod
    def get_payment_url_with_pidx(self, payment_method, pidx, *args, **kwargs):
        pass

    @abstractmethod
    def payment_initiate(self, payment_method, *args, **kwargs):
        pass

    @abstractmethod
    def payment_verify(self, payment_method, **kwargs):
        pass
