# -*- coding: utf-8 -*-
'''
Created on 15 mar 2014

@author: dominika
'''
from py2neo import node, rel, neo4j
from andip.default import DefaultProvider 
class GraphProvider(DefaultProvider):
    def __init__(self, url, backoff=None):
        DefaultProvider.__init__(self, backoff)
        self.url = url
        self.__nodeCounter = 0
        self.conn = None
        self.connect()
        
    def __isLeaf(self, node):
        children = self.getChildren(node)
        if len(children) == 0:
            return True
        return False
    
    def __getNodeConf(self, origin):
        node = origin
        if node is None:
            return None
        result = [node[1]]
        hasParent = True
        pos = None
        resultDict = {}
        value = None
        while hasParent:
            hasParent = False
            parent = self.getParent(node)
            if len(parent) > 0:
                node = parent[0]
                result.append(node[1])
                pos = node[1]
                hasParent = True
                if value is None:
                        value = node[1]
                else:
                        resultDict[node[1]] = value
                        value = None
        lemma = resultDict["word"]
        del resultDict["word"]
        return (pos, lemma, resultDict)
    
    def _get_conf(self, word):
        nodes = self.getNodes(word)
        if len(nodes) == 0:
            return None
        leaves = []
        for candidate in nodes:
            if self.__isLeaf(candidate):
                leaves.append(candidate)
        if len(leaves) == 0:
            raise LookupError("conf=%s", word)
        result = []
        for leaf in leaves:
            result.append(self.__getNodeConf(leaf))
        return result
    
    def __getLeaf(self, node, criteria):
        if len(criteria) == 0:
            return self.getChildren(node)[0][1]
        for nodeChild in self.getChildren(node):
            if nodeChild[1] in criteria:
                for child in self.getChildren(nodeChild):
                    if child[1] == criteria[nodeChild[1]]:
                        del criteria[nodeChild[1]]
                        return self.__getLeaf(child, criteria)
        return None
    
    def __getWordNode(self, posNode, word):
        for wNode in self.getChildren(posNode):
            if wNode[1] == "word":
                for node in self.getChildren(wNode):
                    if node[1] == word:
                        return node
        return None
    
    def _get_word(self, conf):
        pos = conf[0]
        word = conf[1]
        criteria = conf[2]
        
        posNode = self.getNodes(pos)[0]
        if posNode is None:
            raise LookupError("word=%s", conf)
        wordNode = self.__getWordNode(posNode, word)
        if wordNode is None:
            raise LookupError("word=%s", conf)
        return self.__getLeaf(wordNode, criteria)
    
    def connect(self):
        self.conn = neo4j.GraphDatabaseService(self.url)
    
    def close(self):
        self.conn = None
    
    def node(self, id, data):
        self.nodes.append(node(name=data))
    
    def getNodes(self, criteria):
        nodes = neo4j.CypherQuery(self.conn, "MATCH (a) WHERE a.name='%s' RETURN a" % criteria)
        result = []
        for elem in nodes.stream():
            node = (elem[0]._id, elem[0]["name"])
            result.append(node)
        return result;
            
    def rel(self, startNode, endNode, data):
        rels = [rel(startNode, data, endNode)]
        rels.extend(self.rels)
        self.rels = rels
    
    def graph(self):
        self.nodes = []
        self.rels = []

    def commit(self):
        args = []
        args.extend(self.nodes)
        args.extend(self.rels)
        self.conn.create(*args)
        
    def dropAll(self):
        neo4j.CypherQuery(self.conn, "MATCH (n) OPTIONAL MATCH (n)-[r]-() DELETE n,r").execute()
        
        
    def getParent(self, node):
        nodes = neo4j.CypherQuery(self.conn, "MATCH (a)-[:PARENT]->(b) WHERE ID(a)=%s RETURN b" % node[0])
        result = []
        for elem in nodes.stream():
            node = (elem[0]._id, elem[0]["name"])
            result.append(node)
        return result;
        
    def getChildren(self, node):
        nodes = neo4j.CypherQuery(self.conn, "MATCH (a)-[:CHILD]->(b) WHERE ID(a)=%s RETURN b" % node[0])
        result = []
        for elem in nodes.stream():
            node = (elem[0]._id, elem[0]["name"])
            result.append(node)
        return result;
    
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
        return nodeId
    
    def importData(self, dataDict):
        for elem in dataDict:
            self.connect()
            self.__nodeCounter = 0
            self.graph()
            self._importDict(elem, dataDict[elem])
            self.commit()
            self.close()
