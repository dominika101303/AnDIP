from datetime import datetime
from bulbs.titan import Config, TitanClient, Graph

DEFAULT_SERVER="http://localhost:8182/graphs/graph"

config=Config(DEFAULT_SERVER)
graph = graph=Graph(config)
client = TitanClient(config);

def titan_read():
    start = datetime.now()
    for doc in graph.vertices.index.lookup(cls="1"):
        continue
    stop = datetime.now()
    return stop - start

def titan_insert():
    start = datetime.now()
    graph=Graph(config)
    b = graph.vertices.create({"name":"Bruce Willis", "cls":"1"})
    m = graph.vertices.create({"name":"John McClane", "cls":"1"})
    a = graph.vertices.create({"name":"Alan Rickman", "cls":"1"})
    h = graph.vertices.create({"name":"Hans Gruber", "cls":"1"})
    n = graph.vertices.create({"name":"Nakatomi Plaza", "cls":"1"})
    graph.edges.create(b, "PLAYS", m)
    graph.edges.create(a, "PLAYS", h)
    graph.edges.create(b, "VISITS", n)
    graph.edges.create(h, "STEALS_FROM", n)
    graph.edges.create(m, "KILLS", h)
    stop = datetime.now()
    return stop - start
    
def titan_delete():
    start = datetime.now()
    graph.gremlin.execute("g.V.each{g.removeVertex(it)}; ")
    stop = datetime.now()
    return stop - start

read = []
insert = []
delete = []
for i in range(1000):
    print "progress: %d/1000" % i
    insert.append(titan_insert().total_seconds())
    read.append(titan_read().total_seconds())
    delete.append(titan_delete().total_seconds())
    
print "insert: %f" % ( sum(insert)/len(insert) )
print "read: %f" % ( sum(read)/len(read) )
print "delete: %f" % ( sum(delete)/len(delete) )

# insert: 0.069329
# read: 0.059577
# delete: 0.174705