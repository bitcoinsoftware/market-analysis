import BeautifulSoup
import re

import supportFunctions
import AliexpressVolumeCounter


class CategoryScanner:
    def __init__(self):
        self.typeName = 'class'
        self.searchAim = 'div'
        self.className = 'item'
        self.pageNumber = 1
        self.moreBoughtProductsAhead = True
        self.volumeCounter = AliexpressVolumeCounter.VolumeCounter()

    def sanitizeUrl(self, productsPageLink):
        """Removes unnecessary rest of the url"""
        stringToFind = 'html'
        idx = productsPageLink.find(stringToFind) + len(stringToFind)
        return productsPageLink[:idx]

    def getSortedProductsAtPageNumber(self, productsPageLink, pageNumber):
        """There have to be '.html' part removed from basic link and added additional query"""
        query = '.html?site=glo&shipCountry=PL&g=y&SortType=total_tranpro_desc&needQuery=n&tag='

        return productsPageLink[:-5] + '/' + str(pageNumber) + query

    # def getPromotedProductsList(self, soup):
    #     featuredProducts = soup.find('section', attrs={'id' : "featured-offers", 'class': "offers"})
    #     if featuredProducts is not None:
    #         featuredProductsList = featuredProducts.findAll( self.searchAim, attrs={self.typeName : self.className})
    #     else:
    #         featuredProductsList =[]
    #     return featuredProductsList

    def getProductsList(self, soup):
        offersSection = soup.findAll('div', attrs={'id': "list-items"})
        productsList = []
        for offerSec in offersSection:
            productsList += offerSec.findAll(self.searchAim, attrs={self.typeName: self.className})
        return productsList

    def getCategoryTradeVolume(self, categoryPageLink):
        categoryTradeVolume = 0
        categoryPageLink = self.sanitizeUrl(categoryPageLink)

        while self.moreBoughtProductsAhead == True:
            sortedProductsPageLink = self.getSortedProductsAtPageNumber(categoryPageLink, self.pageNumber)
            print "Downloading page: ", sortedProductsPageLink
            pageContent = supportFunctions.downloadWebPageContent(sortedProductsPageLink)
            soup = BeautifulSoup.BeautifulSoup(pageContent)
            listOfProductsOnPage = self.getProductsList(soup)
            numberOfProducts = len(listOfProductsOnPage)
            print numberOfProducts
            if numberOfProducts > 0:
                # numberOfPromotedProducts = len(self.getPromotedProductsList(soup))
                isLastProductSold, pageTradeVolume = self.volumeCounter.getProductListStats(listOfProductsOnPage, categoryLink = categoryPageLink)
                categoryTradeVolume += pageTradeVolume
                if isLastProductSold == True:
                    self.moreBoughtProductsAhead = True
                    self.pageNumber += 1
                else:
                    self.moreBoughtProductsAhead = False
            else:
                self.moreBoughtProductsAhead = False
        return categoryTradeVolume

    def getCategoryMaskValues(self, categoryPageSoup, categoryPageLink):
        # filters = categoryPageSoup.findAll('a', attrs= { 'class' : 'param-toggle filter' })
        categoryMasksLinks = []
        # TODO
        for filter in categoryPageSoup.findAll('a', attrs={'id': re.compile('^param-a_mask')}):
            if filter != None:
                categoryMasksLinks.append(("http://allegro.pl" + filter.get('href'), filter.get('id')))

        if categoryMasksLinks == []:
            categoryMasksLinks = [(categoryPageLink, 0)]
        return categoryMasksLinks


if __name__ == '__main__':
    cs = CategoryScanner()

    categoryUrl = "http://www.aliexpress.com/premium/category/200084017.html?d=n&isViewCP=y&CatId=200084017&catName=mobile-phone-accessories&spm=2114.01020108.0.52.tqaaHV&site=glo&SortType=total_tranpro_desc&shipCountry=pl&g=y&needQuery=n&tag="

    tradeVolume = cs.getCategoryTradeVolume(categoryUrl)

    print 'Wolument sprzedazy %s z dzialu %s ' % (tradeVolume, categoryUrl)
