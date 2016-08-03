from ProductClassifier import *
import supportFunctions


class VolumeCounter:
    def __init__(self):
        pass

    def getBidAmount(self, articleSoup):
        #TODO: bardzo buggy, cos trzeba bedzie z tym zrobic
        ordersHtml = articleSoup.find('em', attrs={'title': 'Total Orders'})
        if ordersHtml is not None:
            ordersText = ordersHtml.text
            ordersAmount = supportFunctions.parseFirstNumber(ordersText)
            if len(ordersAmount) > 0:
                return int(ordersAmount)
        return 0

    def getPrice(self, articleSoup):
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

    def getProductListStats(self, listOfProductsOnPage, categoryLink):
        tradeVolume = 0
        productTradeVolume = 0
        for product in listOfProductsOnPage:
            productTradeVolume = self.getProductTradeVolume(product)
            # productClassifier = ProductClassifier(product, price = self.getPrice(product), categoryLink = categoryLink)
            # productCoordinates = productClassifier.getValues()
            # print productClassifier.getProductInfo()
            tradeVolume += productTradeVolume
        # lastProductSold = self.getBidAmount(listOfProductsOnPage[-1].find('span', attrs={'class' : 'bid-count'}))
        return productTradeVolume > 0, tradeVolume

    def getProductTradeVolume(self, productHtml):
        price = self.getPrice(productHtml)
        amount = self.getBidAmount(productHtml)
        return price * amount
