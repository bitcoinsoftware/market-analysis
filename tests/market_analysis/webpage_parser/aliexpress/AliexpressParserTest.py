import unittest

import BeautifulSoup
from mock import MagicMock

from market_analysis.product.Product import Product
from market_analysis.webpage_parser.aliexpress.AliexpressCategoryParser import AliexpressCategoryParser
from market_analysis.webpage_parser.aliexpress.AliexpressProductParser import AliexpressProductParser


class AliexpressParserTest(unittest.TestCase):
    def setUp(self):
        self.aliexpressProductParser = AliexpressProductParser()
        self.aliexpressCategoryParser = AliexpressCategoryParser(self.aliexpressProductParser)
        self.testProperties = TestProperties()

        self.__initMocks()

    def __initMocks(self):
        f = open("aliexpress-webpage.html", 'r')
        self.aliexpressCategoryParser._fetchProductsSortedByOrderHtml = MagicMock(return_value=BeautifulSoup.BeautifulSoup(f))

    def test_amount_of_found_products(self):
        products = self.aliexpressCategoryParser.getProductsList("", startingPageNumber=1, endingPageNumber=1)
        self.assertEqual(self.testProperties.expectedNrOfProducts, len(products))

    def test_products_details(self):
        products = self.aliexpressCategoryParser.getProductsList("", startingPageNumber=1, endingPageNumber=1)
        self.assertEqual(self.testProperties.expectedProduct1.name, products[0].name)
        self.assertEqual(self.testProperties.expectedProduct1.orders, products[0].orders)
        self.assertEqual(self.testProperties.expectedProduct1.price, products[0].price)
        self.assertEqual(self.testProperties.expectedProduct1.dealVolume, products[0].dealVolume)
        self.assertEqual(self.testProperties.expectedProduct2.name, products[1].name)
        self.assertEqual(self.testProperties.expectedProduct2.orders, products[1].orders)
        self.assertEqual(self.testProperties.expectedProduct2.price, products[1].price)
        self.assertEqual(self.testProperties.expectedProduct2.dealVolume, products[1].dealVolume)


class TestProperties:
    def __init__(self):
        self.pathToHtml="aliexpress-webpage.html"
        self.expectedNrOfProducts=3
        self.expectedProduct1 = []
        self.expectedProduct2 = []
        self.initExpectedProducts()

    def initExpectedProducts(self):
        self.expectedProduct1 = Product()
        self.expectedProduct1.name = "Bastec USB Data Charger Cable Nylon Braided Wire Metal Plug Micro USB Cable for iPhone 6 6s Plus 5s 5 iPad mini Samsung Sony HTC"
        self.expectedProduct1.orders = 72920
        self.expectedProduct1.price = 1.49
        self.expectedProduct1.dealVolume = self.expectedProduct1.orders * self.expectedProduct1.price

        self.expectedProduct2 = Product()
        self.expectedProduct2.name = "Original Baixin 0.3mm 2.5D Tempered Glass Screen Protector For iPhone 5 5S 5c SE HD Toughened Protective Film + Cleaning Kit"
        self.expectedProduct2.orders = 72920
        self.expectedProduct2.price = 0.75
        self.expectedProduct2.dealVolume = self.expectedProduct2.orders * self.expectedProduct2.price

