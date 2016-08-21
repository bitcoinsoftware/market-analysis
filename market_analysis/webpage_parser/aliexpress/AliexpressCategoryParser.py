from market_analysis.webpage_parser.AbstractCategoryParser import AbstractCategoryParser


class AliexpressCategoryParser(AbstractCategoryParser):
    """Aliexpress category parser"""
    _remaining_query_for_sorted_products_by_order = \
        '.html?site=glo&shipCountry=PL&g=y&SortType=total_tranpro_desc&needQuery=n&tag='

    def __init__(self, aliexpressProductParser):
        AbstractCategoryParser.__init__(self, aliexpressProductParser)

    def _getUrlForSortedProductsByOrder(self, pageNumber=1):
        return self.categoryUrl[:-5] + '/' + str(pageNumber) + \
               AliexpressCategoryParser._remaining_query_for_sorted_products_by_order

    def _sanitizeUrl(self, productsPageLink):
        """Removes unnecessary rest of the url"""
        stringToFind = 'html'
        idx = productsPageLink.find(stringToFind) + len(stringToFind)
        return productsPageLink[:idx]

    def _fetchProductsListHtml(self, soup):
        productsHtml = []
        productSections = soup.findAll('div', attrs={'id': 'list-items'})
        for productSection in productSections:
            for productHtml in productSection.findAll('div', attrs={'class': 'item'}):
                productsHtml.append(productHtml)
        return productsHtml


if __name__ == '__main__':
    from market_analysis.webpage_parser.aliexpress.AliexpressProductParser import AliexpressProductParser

    aliexpressProductParser = AliexpressProductParser()
    aliexpressCategoryParser = AliexpressCategoryParser(aliexpressProductParser)
    categoryUrl = "http://www.aliexpress.com/premium/category/200084017.html?d=n&isViewCP" \
                  "=y&CatId=200084017&catName=mobile-phone-accessories&spm=2114.01020108.0.52.tqaaHV&site=glo&" \
                  "SortType=total_tranpro_desc&shipCountry=pl&g=y&needQuery=n&tag="

    products = aliexpressCategoryParser.getProductsList(categoryUrl, startingPageNumber=1, endingPageNumber=3,
                                                        numberOfProductsToProcess=5)
    print 'liczba produktow %s' % len(products)

