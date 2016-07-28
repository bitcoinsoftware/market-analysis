import json, time
import CategoryScanner

class CategoryTreeAnalyzer:
    def __init__(self):
        self.leafesLinks=[]
        self.leafVolumes=[]

    #Return links to the lowest level category 
    def findLeafCategories(self, categoryTreeJson, parentKey):
        #print categoryTreeJson.keys()
        if categoryTreeJson.keys() == [u'i', u'orderMark']: #if it's the lowest level
            self.leafesLinks.append(parentKey)
        else:
            for key in categoryTreeJson.keys():
                if key not in [u'i', u'orderMark']:
                    self.findLeafCategories(categoryTreeJson[key], key)
                    
    def scanLeafCategories(self, outUrl, startLine=0):
        if startLine!=0:
            f = open(outUrl, "a")
        else:
            f = open(outUrl, "w")
        f.close()
        roundNumber = len(self.leafesLinks)
        for link in self.leafesLinks[startLine:]:
            cs = CategoryScanner.CategoryScanner()
            volume = cs.getCategoryTradeVolume("http://allegro.pl"+link)
            self.leafVolumes.append(volume)
            self.saveMarketData(outUrl, link, volume)
            roundNumber = roundNumber - 1
            print link, "WOLUME ", volume
            print "Waiting 2 second. ", roundNumber-startLine, " rounds left"
            time.sleep(2)

    def getFileLineNumber(self, leafCategoryVolumesUrl):
        lines=0
        with open(leafCategoryVolumesUrl) as lCVf:
            lines = lCVf.readlines()
        return len(lines)

    def saveMarketData(self, outUrl, link, volume):
        with open(outUrl ,'a') as f:
            f.write(link + ',' + str(volume) + '\n')

if __name__ == '__main__':
    with open("categoryMap.dat") as fs:
        categoryTreeJson = json.loads(fs.read())
        cta = CategoryTreeAnalyzer()
        cta.findLeafCategories(categoryTreeJson, 'root')
        url = "leafCategoryVolumes.dat"
        lineNumber = cta.getFileLineNumber(url)
        cta.scanLeafCategories(url, lineNumber)
