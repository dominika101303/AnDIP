'''
Created on 15 mar 2014

@author: dominika
'''
from Adapter import Adapter

from py2neo import node, rel, neo4j
from Node import Node
class Neo4jAdapter(Adapter):
    
    def __init__(self, configuration):
        self.__configuration = configuration
        self.url = configuration["url"]
        self.conn = None
                                  
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
            node = Node(elem[0]._id, elem[0]["name"])
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
        nodes = neo4j.CypherQuery(self.conn, "MATCH (a)-[:PARENT]->(b) WHERE ID(a)=%s RETURN b" % node.id)
        result = []
        for elem in nodes.stream():
            node = Node(elem[0]._id, elem[0]["name"])
            result.append(node)
        return result;
        
    def getChildren(self, node):
        nodes = neo4j.CypherQuery(self.conn, "MATCH (a)-[:CHILD]->(b) WHERE ID(a)=%s RETURN b" % node.id)
        result = []
        for elem in nodes.stream():
            node = Node(elem[0]._id, elem[0]["name"])
            result.append(node)
        return result;

