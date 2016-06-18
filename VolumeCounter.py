from ProductClassifier import *
import supportFunctions

class VolumeCounter:
    def __init__(self):
        pass

    def getBidAmount(self, articleSoup):
        bidSpan = articleSoup.find('span', attrs={'class' : 'bid-count'})
        if bidSpan.span is not None:
            spanText = bidSpan.span.text
            splitedSpanText = spanText.split()
            if len(splitedSpanText)>0 and splitedSpanText[0].isdigit():
                if bidSpan.text[-len('licytuje'):] == 'licytuje':
                    return 1
                else:
                    return int(splitedSpanText[0])
            else:
                return 0
        else:
            return 0

    def getPrice(self, articleSoup):
        priceDiv = articleSoup.find('div' , attrs={'class' : 'offer-price'})
        statementSpan = priceDiv.find('span' , attrs={'class' : 'statement'})
        priceStr = supportFunctions.deleteNotNumeric(statementSpan.text)
        if len(priceStr)>0:
            return float(priceStr)
        else:
            return 0

    def getProductListStats(self, listOfProductsOnPage, categoryLink ):
        tradeVolume = 0
        productTradeVolume = 0
        for product in listOfProductsOnPage:
            productTradeVolume = self.getProductTradeVolume(product)
            productClassifier = ProductClassifier(product, price = self.getPrice(product), categoryLink = categoryLink)
            productCoordinates = productClassifier.getValues()
            print productCoordinates
            tradeVolume += productTradeVolume
        #lastProductSold = self.getBidAmount(listOfProductsOnPage[-1].find('span', attrs={'class' : 'bid-count'}))
        return productTradeVolume > 0, tradeVolume

    def getProductTradeVolume(self, productHtml):
        price =  self.getPrice(productHtml)
        amount = self.getBidAmount(productHtml)
        return price * amount

