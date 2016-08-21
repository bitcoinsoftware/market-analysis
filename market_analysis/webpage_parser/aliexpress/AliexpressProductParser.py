import supportFunctions
from market_analysis.webpage_parser.AbstractProductParser import AbstractProductParser


class AliexpressProductParser(AbstractProductParser):
    def __init__(self):
        AbstractProductParser.__init__(self)

    def _fetchName(self, productHtml):
        nameHtml = productHtml.find('a', attrs={'class': 'product '})
        return nameHtml['title']

    def _fetchOrders(self, productHtml):
        ordersHtml = productHtml.find('em', attrs={'title': 'Total Orders'})
        if ordersHtml is not None:
            ordersText = ordersHtml.text
            ordersAmount = supportFunctions.parseFirstNumber(ordersText)
            if len(ordersAmount) > 0:
                return int(ordersAmount)
        return 0

    def _fetchPrice(self, productHtml):
        priceDiv = productHtml.find('span', attrs={'class': 'value', 'itemprop': 'price'})
        text = priceDiv.text
        i = text.find("$")
        if i != -1:
            text = text[i + 1:]

        # TODO: konwersja do PLN na podstawie kursu z dnia dzisiejszego
        priceStr = supportFunctions.parseFirstNumber(text)

        if len(priceStr) > 0:
            return float(priceStr)
        else:
            return 0

