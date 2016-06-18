import urllib2


def downloadWebPageContent(webPageUrl, fileNameUrl = None):
    user_agent = 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_4; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.472.63 Safari/534.3'
    headers = { 'User-Agent' : user_agent }
    req = urllib2.Request(webPageUrl, None, headers)
    response = urllib2.urlopen(req)
    pageContent = response.read()
    if fileNameUrl is not None:
        with open(fileNameUrl , 'w') as f:
            f.write(pageContent)
    return pageContent

def deleteNotNumeric(text):
    text = text.replace("6&nbsp;", "").replace(',', '.')
    newText = ""
    for letter in text:
        if letter.isdigit() or letter == '.':
            newText += letter
    return newText