from abc import ABCMeta, abstractmethod

import BeautifulSoup
import logging
import supportFunctions
from AbstractProductParser import AbstractProductParser


class AbstractCategoryParser:
    """Abstract class for parsing products from web pagey"""
    __metaclass__ = ABCMeta

    def __init__(self, productAnalyzer):
        """productAnalyzer : AbstractProductAnalyzer"""
        assert isinstance(productAnalyzer, AbstractProductParser)
        self.logger = logging.getLogger(AbstractCategoryParser.__name__)
        self.categoryUrl = None
        self.productParser = productAnalyzer

    def getProductsList(self, categoryUrl, startingPageNumber=1, endingPageNumber=None, numberOfProductsToProcess=None):
        """Returns list of products"""
        self.categoryUrl = categoryUrl
        self.categoryUrl = self._sanitizeUrl(self.categoryUrl)
        products = []

        nextPageToProcess = True
        pageNumber = startingPageNumber

        while nextPageToProcess:
            pageHtml = self._fetchProductsSortedByOrderHtml(pageNumber)
            productsListHtml = self._fetchProductsListHtml(pageHtml)

            if len(productsListHtml) == 0:
                nextPageToProcess = False
            else:
                for productHtml in productsListHtml:
                    product = self.__getProductFromProductHtml(productHtml)

                    if product.orders == 0:  # there are no products left
                        nextPageToProcess = False
                        break
                    products.append(product)
                    if numberOfProductsToProcess and len(products) >= numberOfProductsToProcess:
                        nextPageToProcess = False
                        break

                pageNumber += 1
                if endingPageNumber and pageNumber > endingPageNumber:
                    nextPageToProcess = False

        return products

    def _fetchProductsListHtml(self, soup):
        """Returns list of products in html from web page

        soup : BeautifulSoap"""
        pass

    def _sanitizeUrl(self, categoryUrl):
        """Override if url has to be sanitized"""
        return self.categoryUrl

    @abstractmethod
    def _getUrlForSortedProductsByOrder(self, pageNumber=1):
        """Returns url for web page with sorted products by order.

        Second parameter indicates from which page number it should be taken
        Method should return url for that page"""
        pass

    def __getProductFromProductHtml(self, productHtml):
        return self.productParser.getProduct(productHtml)

    def _fetchProductsSortedByOrderHtml(self, pageNumber=1):
        """Returns BeautifulSoup for products sorted by order at given page number"""
        sortedProductsUrl = self._getUrlForSortedProductsByOrder(pageNumber)
        self.logger.debug('Downloading page : ' + sortedProductsUrl)
        pageContent = supportFunctions.downloadWebPageContent(sortedProductsUrl)
        return BeautifulSoup.BeautifulSoup(pageContent)
