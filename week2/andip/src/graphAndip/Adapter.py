'''
Created on 15 mar 2014

@author: dominika
'''
class Adapter(object):
    
    def __init__(self, configuration):
        self.__configuration = configuration
        self.__nodeCounter = 0
                                  
    def connect(self):
        raise NotImplementedError("abstract method")
    
    def close(self):
        raise NotImplementedError("abstract method")
    
    def node(self, id, data):
        raise NotImplementedError("abstract method")
    
    def getNodes(self, criteria):
        raise NotImplementedError("abstract method")
    
    def rel(self, startNode, endNode, data):
        raise NotImplementedError("abstract method")
    
    def graph(self):
        raise NotImplementedError("abstract method")
    
    def commit(self):
        raise NotImplementedError("abstract method")

    def importData(self, dataDict):
        for elem in dataDict:
            self.connect()
            self.__nodeCounter = 0
            self.graph()
            self._importDict(elem, dataDict[elem])
            self.commit()
            self.close()
    
    def dropAll(self):
        raise NotImplementedError("abstract method")
    
    def _importDict(self, name, dataDict):
        self.node(self.__nodeCounter,name)
        nodeId = self.__nodeCounter
        self.__nodeCounter += 1
        for key in dataDict:
            if type(dataDict[key]) is dict:
                childId = self._importDict(key, dataDict[key])
            else:
                valueId= self.__nodeCounter
                self.node(valueId, dataDict[key])
                self.__nodeCounter+=1
                childId= self.__nodeCounter
                self.node(childId, key)
                self.__nodeCounter+=1
                self.rel(childId, valueId, "CHILD")
                self.rel(valueId, childId, "PARENT")
            self.rel(nodeId, childId, "CHILD")
            self.rel(childId, nodeId, "PARENT")
            #self.__nodeCounter += 1
        return nodeId
    
    def getParent(self, node):
        raise NotImplementedError("abstract method")
        
    def getChildren(self, node):
        raise NotImplementedError("abstract method")