from income_analyzer.AbstractIncomeAnalyzer import AbstractIncomeAnalyzer


class AliexpressIncomeAnalyzer(AbstractIncomeAnalyzer):
    """Aliexpress category income analyzer"""
    _remaining_query_for_sorted_products_by_order = \
        '.html?site=glo&shipCountry=PL&g=y&SortType=total_tranpro_desc&needQuery=n&tag='

    def __init__(self, aliexpressProductAnalyzer):
        AbstractIncomeAnalyzer.__init__(self, aliexpressProductAnalyzer)

    def _getUrlForSortedProductsByOrder(self, pageNumber=1):
        return self.categoryUrl[:-5] + '/' + str(pageNumber) + \
               AliexpressIncomeAnalyzer._remaining_query_for_sorted_products_by_order

    def _getOffersSection(self, soup):
        return soup.findAll('div', attrs={'id': 'list-items'})

    def _getSingleProductFromOffer(self, soup):
        return soup.findAll('div', attrs={'class': 'item'})

    def _sanitizeUrl(self, productsPageLink):
        """Removes unnecessary rest of the url"""
        stringToFind = 'html'
        idx = productsPageLink.find(stringToFind) + len(stringToFind)
        return productsPageLink[:idx]


if __name__ == '__main__':
    from income_analyzer.aliexpress.AliexpressProductAnalyzer import AliexpressProductAnalyzer
    apa = AliexpressProductAnalyzer()
    aia = AliexpressIncomeAnalyzer(apa)
    categoryUrl = "http://www.aliexpress.com/premium/category/200084017.html?d=n&isViewCP" \
                  "=y&CatId=200084017&catName=mobile-phone-accessories&spm=2114.01020108.0.52.tqaaHV&site=glo&" \
                  "SortType=total_tranpro_desc&shipCountry=pl&g=y&needQuery=n&tag="
    categoryIncome, nrOfProducts = aia.getCategoryIncome(categoryUrl, startingPageNumber=1, endingPageNumber=3)
    print 'Wolument sprzedazy %s z dzialu %s \n za %s produktow' % (categoryIncome, categoryUrl, nrOfProducts)
