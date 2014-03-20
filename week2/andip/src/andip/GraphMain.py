# -*- coding: utf-8 -*-
from neo4j import GraphProvider
import json

data = eval(open("../../data/polish.txt").read())

conf = "http://localhost:7474/db/data/"

provider =  GraphProvider(conf)

provider.dropAll()
#provider.importData(data)
provider.connect()
print provider.get_conf('ja')
print provider.get_word(('czasownik', 'być', {'forma': 'czas teraźniejszy', 'liczba': 'pojedyncza', 'osoba': 'trzecia'}))