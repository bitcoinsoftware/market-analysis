from BeautifulSoup import BeautifulSoup

def getBidAmount(articleSoup):
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

def deleteNotNumeric(text):
    text = text.replace("6&nbsp;", "").replace(',', '.')
    newText=""
    for letter in text:
        if letter.isdigit() or letter=='.':
            newText += letter
    return newText

def getPrice(articleSoup):
    #<div class="offer-price">
    priceDiv = articleSoup.find('div' , attrs={'class' : 'offer-price'})
    statementSpan = priceDiv.find('span' , attrs={'class' : 'statement'})
    priceStr = deleteNotNumeric(statementSpan.text)
    if len(priceStr)>0:
        return float(priceStr)
    else:
        return 0

with open('laptopy.html') as f:
    soup = BeautifulSoup(f.read())
    featuredProducts = soup.find('section', attrs={'class': "offers"})
    featuredProductsList = featuredProducts.findAll( 'article', attrs={'class' : 'offer'})
    #print featuredProductsList[-1].find('span', attrs={'class' : 'bid-count'}).span
    product = featuredProductsList[10]
    print getPrice(product)
    print getBidAmount(product)
    print "Volume ",  getPrice(product) *  getBidAmount(product)

