from datetime import datetime


from py2neo import node, rel, neo4j
graph_db = neo4j.GraphDatabaseService("http://localhost:7474/db/data/")

def titan_read():
    start = datetime.now()
    neo4j.CypherQuery(graph_db, "MATCH (n) return n").execute()
    stop = datetime.now()
    return stop - start

def titan_insert():
    start = datetime.now()
    die_hard = graph_db.create(
    node(name="Bruce Willis"),
    node(name="John McClane"),
    node(name="Alan Rickman"),
    node(name="Hans Gruber"),
    node(name="Nakatomi Plaza"),
    rel(0, "PLAYS", 1),
    rel(2, "PLAYS", 3),
    rel(1, "VISITS", 4),
    rel(3, "STEALS_FROM", 4),
    rel(1, "KILLS", 3),
    )
    stop = datetime.now()
    return stop - start
    
def titan_delete():
    start = datetime.now()
    neo4j.CypherQuery(graph_db, "MATCH (n) OPTIONAL MATCH (n)-[r]-() DELETE n,r").execute()
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

# insert: 0.066496 (66,5 s)
# read: 0.082711   (82,3 s)
# delete: 0.125977  (126 s )