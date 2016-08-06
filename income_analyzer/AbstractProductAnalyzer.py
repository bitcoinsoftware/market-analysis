from abc import ABCMeta, abstractmethod


class AbstractProductAnalyzer:
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    def getProductIncome(self, product):
        price = self._getPrice(product)
        amount = self._getBidAmount(product)
        return price * amount

    @abstractmethod
    def _getPrice(self, product):
        pass

    @abstractmethod
    def _getBidAmount(self, product):
        pass

