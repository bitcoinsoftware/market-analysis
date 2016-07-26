import datetime
import sys
import BeautifulSoup
import supportFunctions

from pprint import pprint

class CategoryTree:
    def __init__(self):
        self.typeName = 'class'
        self.searchAim = 'a'
        self.aimLevels2 = ['alleLink lvl0', 'alleLink lvl1', 'alleLink lvl2', 'alleLink lvl3', 'alleLink lvl4', 'alleLink lvl5']
        #self.aimLevels2 = ['alleLink lvl1', 'alleLink lvl2']#, 'alleLink lvl3', 'alleLink lvl4', 'alleLink lvl5']
        self.leafesLinks=[]

    def getCategoryLinks(self, categoryPageContent, aim):
        soup = BeautifulSoup.BeautifulSoup(categoryPageContent)
        links = soup.findAll( self.searchAim, attrs={self.typeName : aim} )
        pairs =[]
        for link in links:
            position = str(categoryPageContent).rfind(str(link))
            pairs.append((str(link['href']), {'i':position}))
        return pairs

    def getSubDict(self, childrenDict, parent, next_parent):
        subDict = {}
        #for node in nodes:
        #testDupa = 1
        for key in childrenDict.keys():
            #node_position, parent_position, next_parent_position = node[0], parent[0], next_parent[0]
            if key !='i' and key != None:
                node_position, parent_position, next_parent_position = childrenDict[key]['i'], parent[1]['i'], next_parent[1]['i']
                if node_position > parent_position and node_position < next_parent_position:
                    try:
                        subDict[key] = childrenDict[key]
                    except:
                        subDict[key] = {'i' : node_position}

                #elif node_position > next_parent_position:
                #    print "STOP, ",key," ", childrenDict[key] , " za daleko, przekroczylo", next_parent
                #    break
                #print node_position ,' > ', parent_position, ' and ', node_position, ' < ', next_parent_position# , key
        #if testDupa: print " NIC NIE WESZLO"
        return subDict
#TODO slowniki sie nie lacza, problem z dziedziczeniem
    def getCategoryTree(self, categoryPageContent):
        #first get the links:
        nodes = []
        for aim in self.aimLevels2:
            print "Agregating nodes containing aim : ", aim
            nodes.append(self.getCategoryLinks(categoryPageContent, aim))
        print "Nodes selected, total lvls ", len(nodes)
        mainTree = {'root':{}}
        lvl_number = len(nodes)
        if lvl_number > 1:
            childrenDict = None

            for lvl in xrange(len(nodes)-1, 0, -1): # reversed range
                print "Analyzing lvl ", lvl , " with number of nodes : ", len(nodes[lvl])
                if childrenDict is None:
                    print "Generating Children Dict from list of ", len(nodes[lvl]), " elements"
                    childrenDict = dict(nodes[lvl])

                parent_node_list = nodes[ lvl - 1 ]
                print "Potential parent nodes from lvl ", lvl - 1, " : ", len(parent_node_list)
                parentDict = {}
                for i in xrange(1,len(parent_node_list)):
                    parent_node, next_parent_node = parent_node_list[i-1], parent_node_list[i]
                    try:
                        parentDict[parent_node[0]].update( self.getSubDict(childrenDict, parent_node, next_parent_node))
                    except KeyError:
                        parentDict[parent_node[0]] = self.getSubDict(childrenDict, parent_node, next_parent_node)
                    parentDict[parent_node[0]]['i'] = parent_node[1]['i']
                childrenDict = parentDict

            mainTree['root'] = childrenDict
        else :
            for node in nodes:
                mainTree[node[0]] = {}
        return  mainTree

    def addOrderMarks(self, tree, prefix=''):
        if len(tree.keys())>1 or tree.keys()[0]=='root':
            i = 0
            for key in tree.keys():
                if key!='i' and key!='orderMark' :
                    tree[key]['orderMark'] = prefix + str(unichr(i))
                    tree[key] = self.addOrderMarks(tree[key], tree[key]['orderMark'])
                    i += 1
        return tree

    def getTreeWithOrderMarks(self, tree):
        return self.addOrderMarks(tree)

    #Return links to the lowest level category 
    def findLeafCategories(categoryTreeJson):
        for key in categoryTreeJson.keys():
            subTree = categoryTreeJson[key]
            if subTree.keys() == [u'i', u'orderMark']: #if it's the lowest level
                self.leafesLinks.append(key)
            else:
                self.findLeafCategories(subTree)


if __name__ == '__main__':
    import json
    cs = CategoryTree()
    allegroCategoryMapUrl = 'http://allegro.pl/category_map.php'
    outputFile = 'category_map.html'
    #fileNameUrl = str(datetime.datetime.now())
    print "DOWNLOADING PAGE CONTENT"
    pageContent = supportFunctions.downloadWebPageContent(allegroCategoryMapUrl)#, fileNameUrl)
    print "TREE CREATION"
    finalDict = cs.getCategoryTree(pageContent)
    print "INSERTING ORDER MARKS"
    finalDict = cs.getTreeWithOrderMarks(finalDict)

    with open("categoryMap.dat", "w") as f:
        f.write(json.dumps(finalDict))

#    cs.findLeafCategories(finalDict)

    
    
