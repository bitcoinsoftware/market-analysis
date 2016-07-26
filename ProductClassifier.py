"""
This class provides methods for product classification
based on the name , price and category of the product.

"""

import trans
import BeautifulSoup

class ProductClassifier:
    def __init__(self, productSoup, price, categoryLink):
        self.soup = productSoup
        self.priceVal = price
        self.categoryVal = 0
        self.subjectVal = 0
        self.paramsVal = 0

        self.getCategoryVal(categoryLink)
        self.getSubjectVal(self.getSubjectName(productSoup))
        self.getParamsVal(productSoup)

    def getParamsVal(self, productSoup):
        soup = BeautifulSoup.BeautifulSoup(str(productSoup))
        params = soup.find('div', attrs = {'class' : 'offer-attributes'})
        result =[]
        if params != None:
            params = params.findAll('dd')
            for param in params:
                if param.span != None:
                    try:
                        #print param.span.text
                        result.append(str( param.span.text ))
                    except:
                        print "ERROR: ", param.span
        self.paramsVal = self.getSplitedTextValue(result)

    def getCategoryVal(self, categoryLink):
        splitedLink = categoryLink.split('-')
        try:
            self.categoryVal = int(splitedLink[-1])
        except:
            pass

    def getSubjectVal(self, subject):
        enSubject = str(trans.trans(unicode(subject))).upper()
        splitedSubject = enSubject.split()
        self.subjectVal = self.getSplitedTextValue(splitedSubject)

    def getSplitedTextValue(self, splitedText):
        """
        T - product title from the listing
        X = uppercase(T)
        X = x1 + x2 ... + xn where x1 is a word
        S(X) = SUM_from_i=0_to_n(X) ( f(x_i))
        f(x_i) = SUM_from_j=0_to_n(x) ( valueSpace ^j *ord(x_i) )
        """
        val =0
        valueSpaceSize = abs( ord('Z') - ord('0'))
        for word in splitedText:
            for j in xrange(len(word)):
                val += valueSpaceSize **j * ord(word[j])
        return val

    def getSubjectName(self, productSoup):
        soup = BeautifulSoup.BeautifulSoup(str(productSoup))
        title = soup.find('div', attrs = { 'class' : 'offer-info' }).find('a').text
        return title

    def getValues(self):
        return (self.priceVal, self.categoryVal, self.subjectVal, self.paramsVal)

    def getProductInfo(self):
        return "Price %d [PLN], category number %d, auction subject value %d , auction params value %d" % self.getValues()
