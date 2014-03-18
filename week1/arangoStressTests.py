from datetime import datetime
from arango import create

c = create(db="test")

c.database.create()



def titan_read():
    start = datetime.now()
    for doc in c.test.query.execute():
        continue
    for doc in c.test_edges.query.execute():
        continue
    stop = datetime.now()
    return stop - start

def titan_insert():
    start = datetime.now()
    c.test.create()
    bruce = c.test.documents.create({"name":"Bruce Willis"})
    john = c.test.documents.create({"name":"John McClane"})
    alan = c.test.documents.create({"name":"Alan Rickman"})
    hans = c.test.documents.create({"name":"Hans Gruber"})
    nakatomi = c.test.documents.create({"name":"Nakatomi Plaza"})
    c.test_edges.create_edges()
    c.test_edges.edges.create(bruce,john,{"label": "PLAYS"})
    c.test_edges.edges.create(alan,hans,{"label": "PLAYS"})
    c.test_edges.edges.create(bruce, nakatomi,{"label": "VISITS"})
    c.test_edges.edges.create(hans, nakatomi,{"label":"STEALS_FROM"})
    c.test_edges.edges.create(john, hans, {"label": "KILLS"})
    stop = datetime.now()
    return stop - start
    
def titan_delete():
    start = datetime.now()
    c.test.delete()
    c.test_edges.delete()
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

# insert: 0.508495 (508 s)
# read: 0.015508 (15,5 s)
# delete: 0.089080 (89 s)