from abc import ABCMeta, abstractmethod
import BeautifulSoup
import supportFunctions
from aliexpress import AliexpressProductAnalyzer
from AbstractProductAnalyzer import AbstractProductAnalyzer


class AbstractIncomeAnalyzer:
    """Abstract class for analyzing income for certain category"""
    __metaclass__ = ABCMeta

    def __init__(self, productAnalyzer):
        """productAnalyzer : AbstractProductAnalyzer"""
        assert isinstance(productAnalyzer, AbstractProductAnalyzer)
        self.categoryUrl = None
        self.productAnalyzer = productAnalyzer

    def getCategoryIncome(self, categoryUrl, startingPageNumber=1, endingPageNumber=None):
        """Returns total category income and total number of products which are sold."""
        self.categoryUrl = categoryUrl
        self.categoryUrl = self._sanitizeUrl(self.categoryUrl)

        totalIncome = 0
        totalNumberOfProducts = 0
        moreProductsToProcess = True
        pageNumber = startingPageNumber

        while moreProductsToProcess:
            pageContent = self.__getBeautifulSoupForProductsSortedByOrder(pageNumber)
            listOfProductsOnPage = self._getProductsListFromPage(pageContent)
            nrOfProductsOnPage = len(listOfProductsOnPage)

            if nrOfProductsOnPage > 0:
                totalNumberOfProducts += nrOfProductsOnPage
                isLastProductSold, pageIncome = self.__getPageIncome(listOfProductsOnPage)
                totalIncome += pageIncome
                if isLastProductSold:
                    pageNumber += 1
                    if endingPageNumber:
                        if pageNumber >= endingPageNumber:
                            moreProductsToProcess = False
                else:
                    moreProductsToProcess = False
            else:
                moreProductsToProcess = False
        return totalIncome, totalNumberOfProducts

    def _getProductsListFromPage(self, soup):
        """Returns list of products from the page.

        soup : BeautifulSoup"""
        assert isinstance(soup, BeautifulSoup.BeautifulSoup)
        offersSection = self._getOffersSection(soup)
        productList = []
        for offer in offersSection:
            productList += self._getSingleProductFromOffer(offer)
        return productList

    def _sanitizeUrl(self, categoryUrl):
        """Override if url has to be sanitized"""
        return self.categoryUrl

    @abstractmethod
    def _getUrlForSortedProductsByOrder(self, pageNumber=1):
        """Returns url for web page with sorted products by order.

        Second parameter indicates from which page number it should be taken
        Method should return url for that page"""
        pass

    @abstractmethod
    def _getOffersSection(self, soup):
        """It should return offers section in the page.

        soup : BeautifulSoup
        """
        pass

    @abstractmethod
    def _getSingleProductFromOffer(self, soup):
        """It should return single product from offer.

        soup : BeautifulSoup
        """
        pass

    def __getPageIncome(self, listOfProductsOnPage):
        productIncome = 0
        pageIncome = 0
        for product in listOfProductsOnPage:
            productIncome = self.productAnalyzer.getProductIncome(product)
            pageIncome += productIncome
        return productIncome > 0, pageIncome

    def __getBeautifulSoupForProductsSortedByOrder(self, pageNumber=1):
        """Returns BeautifulSoup for products sorted by order at given page number"""
        sortedProductsUrl = self._getUrlForSortedProductsByOrder(pageNumber)
        print 'Downloading page : ' + sortedProductsUrl
        pageContent = supportFunctions.downloadWebPageContent(sortedProductsUrl)
        return BeautifulSoup.BeautifulSoup(pageContent)

