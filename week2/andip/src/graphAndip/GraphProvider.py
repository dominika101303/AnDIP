# -*- coding: utf-8 -*-
'''
Created on 15 mar 2014

@author: dominika
'''

from andip.default import DefaultProvider 
from exception import *
class GraphProvider(DefaultProvider):
    def __init__(self, adapter, backoff=None):
        DefaultProvider.__init__(self, backoff)
        self.adapter = adapter
        self.adapter.connect()
        
    def __isLeaf(self, node):
        children = self.adapter.getChildren(node)
        if len(children) == 0:
            return True
        return False
    def __getNodeConf(self, origin):
        node = origin
        if node is None:
            return None
        result = [node.name]
        hasParent = True
        pos = None
        resultDict = {}
        value = None
        while hasParent:
            hasParent = False
            parent = self.adapter.getParent(node)
            if len(parent) > 0:
                node = parent[0]
                result.append(node.name)
                pos = node.name
                hasParent = True
                if value is None:
                        value = node.name
                else:
                        resultDict[node.name] = value
                        value = None
        lemma = resultDict["word"]
        del resultDict["word"]
        return (pos, lemma, resultDict)
    
    def _get_conf(self, word):
        nodes = self.adapter.getNodes(word)
        if len(nodes) == 0:
            return None
        leaves = []
        for candidate in nodes:
            if self.__isLeaf(candidate):
                leaves.append(candidate)
        if len(leaves) == 0:
            raise NoSuchConfException("conf=%s", word)
        result = []
        for leaf in leaves:
            result.append(self.__getNodeConf(leaf))
        return result
    
    def __getLeaf(self, node, criteria):
        if len(criteria) == 0:
            return self.adapter.getChildren(node)[0].name
        for nodeChild in self.adapter.getChildren(node):
            if nodeChild.name in criteria:
                for child in self.adapter.getChildren(nodeChild):
                    if child.name == criteria[nodeChild.name]:
                        del criteria[nodeChild.name]
                        return self.__getLeaf(child, criteria)
        return None
    
    def __getWordNode(self, posNode, word):
        for wNode in self.adapter.getChildren(posNode):
            if wNode.name == "word":
                for node in self.adapter.getChildren(wNode):
                    if node.name == word:
                        return node
        return None
    
    def _get_word(self, conf):
        pos = conf[0]
        word = conf[1]
        criteria = conf[2]
        
        posNode = self.adapter.getNodes(pos)[0]
        if posNode is None:
            raise NoSuchWordException("word=%s", conf)
        wordNode = self.__getWordNode(posNode, word)
        if wordNode is None:
            raise NoSuchWordException("word=%s", conf)
        return self.__getLeaf(wordNode, criteria)
