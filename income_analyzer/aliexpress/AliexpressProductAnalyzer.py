import supportFunctions
from income_analyzer.AbstractProductAnalyzer import AbstractProductAnalyzer


class AliexpressProductAnalyzer(AbstractProductAnalyzer):
    def __init__(self):
        AbstractProductAnalyzer.__init__(self)

    def _getBidAmount(self, articleSoup):
        ordersHtml = articleSoup.find('em', attrs={'title': 'Total Orders'})
        if ordersHtml is not None:
            ordersText = ordersHtml.text
            ordersAmount = supportFunctions.parseFirstNumber(ordersText)
            if len(ordersAmount) > 0:
                return int(ordersAmount)
        return 0

    def _getPrice(self, articleSoup):
        priceDiv = articleSoup.find('span', attrs={'class': 'value', 'itemprop': 'price'})
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

