'''
Created on 15 mar 2014

@author: dominika
'''
class Node(object):
    
    def __init__(self, _id, _name):
        self.id = _id
        self.name = _name
        
    def __str__(self):
        return "Node[id=%s, name=%s]" % (self.id, self.name)