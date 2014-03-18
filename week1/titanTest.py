from bulbs.titan import Config, TitanClient, Graph

DEFAULT_SERVER="http://localhost:8182/graphs/graph"

config=Config(DEFAULT_SERVER)
graph=Graph(config)
client = TitanClient(config);

graph.vertices.create({"name":"Bruce Willis"})
graph.vertices.create({"name":"John McClane"})
graph.vertices.create({"name":"Alan Rickman"})
graph.vertices.create({"name":"Hans Gruber"})
graph.vertices.create({"name":"Nakatomi Plaza"})
graph.edges.create(40012, "PLAYS", 40016)
graph.edges.create(40020, "PLAYS", 40024)
graph.edges.create(40016, "VISITS", 40028)
graph.edges.create(40024, "STEALS_FROM", 40028)
graph.edges.create(40016, "KILLS", 40024)