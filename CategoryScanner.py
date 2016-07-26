import urllib2
import BeautifulSoup
import re

import supportFunctions
import VolumeCounter

class CategoryScanner:
    def __init__(self):
        self.typeName  = 'class'
        self.searchAim = 'article'
        self.className = 'offer'
        self.pageNumber = 1
        self.moreBoughtProductsAhead = True
        self.volumeCounter = VolumeCounter.VolumeCounter()

    def getSortedProductsPageLink(self, productsPageLink, pageNumber):
        return productsPageLink + "?order=qd&offerTypeBuyNow=1&p=" + str(pageNumber)

    def getPromotedProductsList(self, soup):
        featuredProducts = soup.find('section', attrs={'id' : "featured-offers", 'class': "offers"})
        if featuredProducts is not None:
            featuredProductsList = featuredProducts.findAll( self.searchAim, attrs={self.typeName : self.className})
        else:
            featuredProductsList =[]
        return featuredProductsList

    def getProductsList(self, soup):
        offersSection = soup.findAll('section', attrs={'class': "offers"})
        productsList =[]
        for offerSec in offersSection:
            productsList += offerSec.findAll( self.searchAim, attrs={self.typeName : self.className})
        return productsList

    def getCategoryTradeVolume(self, categoryPageLink):
        categoryTradeVolume = 0
        while self.moreBoughtProductsAhead == True:
            sortedProductsPageLink = self.getSortedProductsPageLink(categoryPageLink, self.pageNumber)
            print "Downloading page: ", sortedProductsPageLink
            pageContent = supportFunctions.downloadWebPageContent(sortedProductsPageLink)
            soup = BeautifulSoup.BeautifulSoup(pageContent)
            listOfProductsOnPage = self.getProductsList( soup )
            numberOfProducts = len(listOfProductsOnPage)
            if numberOfProducts > 0:
                numberOfPromotedProducts = len(self.getPromotedProductsList(soup))
                isLastProductSold, pageTradeVolume = self.volumeCounter.getProductListStats(listOfProductsOnPage, categoryLink = categoryPageLink)
                categoryTradeVolume += pageTradeVolume
                if isLastProductSold == True or numberOfPromotedProducts == numberOfProducts:
                    self.moreBoughtProductsAhead = True
                    self.pageNumber += 1
                else:
                    self.moreBoughtProductsAhead = False
            else:
                self.moreBoughtProductsAhead = False
        return categoryTradeVolume

    def getCategoryMaskValues(self, categoryPageSoup, categoryPageLink ):
        #filters = categoryPageSoup.findAll('a', attrs= { 'class' : 'param-toggle filter' })
        categoryMasksLinks = []
        #TODO
        for filter in categoryPageSoup.findAll('a', attrs= { 'id' : re.compile('^param-a_mask') }):
            if filter !=None:
                categoryMasksLinks.append(( "http://allegro.pl" + filter.get('href') , filter.get('id') ))

        if categoryMasksLinks == []:
            categoryMasksLinks = [(categoryPageLink, 0)]
        return categoryMasksLinks


if __name__ == '__main__':
    cs = CategoryScanner()
    categoryUrl = 'http://allegro.pl/akcesoria-biurowe-dziurkacze-64641'
    tradeVolume = cs.getCategoryTradeVolume(categoryUrl)

    print "Wolumen sprzedazy %s z dzialu %s "% (tradeVolume, categoryUrl)
