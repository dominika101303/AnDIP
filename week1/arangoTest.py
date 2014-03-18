from arango import create

c = create(db="test")

c.database.create()

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