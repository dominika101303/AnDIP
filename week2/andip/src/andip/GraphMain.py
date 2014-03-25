# -*- coding: utf-8 -*-
from neo4j import GraphProvider
from andip import PlWikiProvider
import json

data = eval(open("../../data/polish.txt").read())

conf = "http://localhost:7474/db/data/"

provider =  GraphProvider(conf)

provider.dropAll()
provider.importData(data)
provider.connect()
print provider.get_conf('ja')
print provider.get_word(('czasownik', 'być', {'forma': 'czas teraźniejszy', 'liczba': 'pojedyncza', 'osoba': 'trzecia'}))
wiki = PlWikiProvider()
provider =  GraphProvider(conf,wiki)
print provider.get_word(('czasownik', 'narysować', {'aspekt': 'dokonane', 'forma': 'czas przyszły', 'liczba': 'pojedyncza', 'osoba': 'pierwsza'}))
print provider.get_conf('narysuję')