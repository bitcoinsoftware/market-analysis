from abc import ABCMeta, abstractmethod

import BeautifulSoup

from market_analysis.product.Product import Product


class AbstractProductParser:
    """Abstract class to parse product from html tags"""
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    def getProduct(self, productHtml):
        assert isinstance(productHtml, BeautifulSoup.Tag)
        product = Product()
        product.name = self._fetchName(productHtml)
        product.price = self._fetchPrice(productHtml)
        product.orders = self._fetchOrders(productHtml)
        product.dealVolume = product.price * product.orders
        return product

    @abstractmethod
    def _fetchName(self, productHtml):
        pass

    @abstractmethod
    def _fetchOrders(self, productHtml):
        pass

    @abstractmethod
    def _fetchPrice(self, productHtml):
        pass
