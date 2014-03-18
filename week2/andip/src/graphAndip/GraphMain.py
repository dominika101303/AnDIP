# -*- coding: utf-8 -*-
from Neo4jAdapter import Neo4jAdapter
from GraphProvider import GraphProvider
import data_pl

data = data_pl.data_pl
conf = {
        "url": "http://localhost:7474/db/data/"
        }

adapter =  Neo4jAdapter(conf)

# adapter.importData(data)
# adapter.close()
# adapter.connect()
# adapter.dropAll()
# adapter.importData(data)
provider = GraphProvider(adapter)
print provider.get_conf('ja')
print provider.get_word(('czasownik', 'być', {'forma': 'czas teraźniejszy', 'liczba': 'pojedyncza', 'osoba': 'trzecia'}))