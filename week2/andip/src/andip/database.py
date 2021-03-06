# -*- coding: utf-8 -*-

from andip.default import DefaultProvider
from ZODB.FileStorage import FileStorage
from ZODB.DB import DB
from persistent.mapping import PersistentMapping
import transaction

class DatabaseProvider(DefaultProvider):

    def __init__(self, path, backoff = None):
        """
        Initializes DatabaseProvider.

        This provider requires closing database after using (call close function).

        :param path: path to a database file
        :type path: str
        :param backoff: (optional) backoff provider
        """
        DefaultProvider.__init__(self, backoff)

        self.storage = FileStorage(path + '.fs')
        self.db = DB(self.storage)
        self.connection = self.db.open()
        self.root = self.connection.root()

        if not self.root:
            self.__dictionary_init()

    def __check_connection(self):
        if self.root == None:
            raise LookupError("Database connection is closed!")

    def close(self):
        """
        Function close connection to database.

        Call this before destroying DatabaseProvider object to avoid issues with database file access.
        """
        self.connection.close()
        self.db.close()
        self.storage.close()
        self.root = None

    def save_model(self, conf):
        """
        Inserts new data into database.

        Get new data using WikiProvider and get it using get_model method.

        :param conf: new data returned by WikiProvider get_model method
        """
        self.__check_connection();

        for type in conf:
            for baseword in  conf[type]:
                self.__save(conf[type][baseword], baseword, type)

    def _get_word(self, conf):
        '''
        Returns word or throw KeyError, if there is no information
        about word in database
        '''
        self.__check_connection();
        return self.__get_word(conf[2], conf[1])

    def _get_conf(self, word):
        '''
        Returns word configuration or KeyError, if there is no
        information about word in database
        '''
        self.__check_connection();
        return self.__get_conf_preview(word)

    def __dictionary_init(self):
        '''
           Initialization of database dictionaries.
        '''
        self.root['przymiotnik'] = PersistentMapping()
        self.root['rzeczownik'] = PersistentMapping()
        self.root['czasownik'] = PersistentMapping()
        self.root['czasownik']['word'] = PersistentMapping()
        self.root['przymiotnik']['word'] = PersistentMapping()
        self.root['rzeczownik']['word'] = PersistentMapping()
        transaction.commit()

    def __save(self, dict, base_word, type):
        '''
            Save object to database in Bartosz Alchimowicz convention
        '''
        self.root[type]['word'][base_word] = dict
        transaction.commit()

    def __get_conf(self, base_word):
        '''
            Get configuration of word whic is in database
        '''
        for word_type in ['rzeczownik', 'czasownik', 'przymiotnik']:
            for word in self.root[word_type]['word'].keys():
                if word == base_word:
                    return self.root[word_type]['word'][word]

        raise KeyError("There is no such a word in Database")

    def __get_conf_preview(self, word):

        # rzeczownik
        dictionary = self.root['rzeczownik']['word']

        for base_word in dictionary.keys():
            for przypadek in dictionary[base_word]['przypadek'].keys():
                for liczba in dictionary[base_word]['przypadek'][przypadek]['liczba'].keys():
                    if dictionary[base_word]['przypadek'][przypadek]['liczba'][liczba] == word:
                        return [('rzeczownik', base_word,
                                {'przypadek' : przypadek,
                                 'liczba' : liczba })]
        # przymiotnik
        dictionary = self.root['przymiotnik']['word']

        for base_word in dictionary.keys():
            for stopien in dictionary[base_word]['stopień'].keys():
                for przypadek in dictionary[base_word]['stopień'][stopien]['przypadek'].keys():
                    for liczba in dictionary[base_word]['stopień'][stopien]['przypadek'][przypadek]['liczba'].keys():
                        for rodzaj in dictionary[base_word]['stopień'][stopien]['przypadek'][przypadek]['liczba'][liczba]['rodzaj'].keys():
                            if dictionary[base_word]['stopień'][stopien]['przypadek'][przypadek]['liczba'][liczba]['rodzaj'][rodzaj] == word:
                                return [('przymiotnik', base_word,
                                        {'stopień' : stopien,
                                         'liczba' : liczba,
                                         'rodzaj' : rodzaj})]
        # czasownik
        dictionary = self.root['czasownik']['word']

        for base_word in dictionary.keys():
            for aspekt in dictionary[base_word]['aspekt'].keys():
                for forma in dictionary[base_word]['aspekt'][aspekt]['forma'].keys():
                    for liczba in dictionary[base_word]['aspekt'][aspekt]['forma'][forma]['liczba'].keys():
                        for osoba in dictionary[base_word]['aspekt'][aspekt]['forma'][forma]['liczba'][liczba]['osoba'].keys():
                            if forma == 'czas przeszły':
                                for rodzaj in dictionary[base_word]['aspekt'][aspekt]['forma'][forma]['liczba'][liczba]['osoba'][osoba]['rodzaj'].keys():
                                    if dictionary[base_word]['aspekt'][aspekt]['forma'][forma]['liczba'][liczba]['osoba'][osoba]['rodzaj'][rodzaj] == word:
                                        return [('czasownik', base_word,
                                                {'aspekt' : aspekt,
                                                'forma' : forma,
                                                'liczba' : liczba,
                                                'osoba' : osoba,
                                                'rodzaj' : rodzaj})]
                            else:
                                if dictionary[base_word]['aspekt'][aspekt]['forma'][forma]['liczba'][liczba]['osoba'][osoba] == word:
                                        return [('czasownik', base_word,
                                                {'aspekt' : aspekt,
                                                'forma' : forma,
                                                'liczba' : liczba,
                                                'osoba' : osoba})]
        raise LookupError("configuration not found")


    def __get_word(self, conf, base_word):
        '''
            Search all database and get word
        '''
        try:
            return self.root['rzeczownik']['word'][base_word]['przypadek'][conf['przypadek']]['liczba'][conf['liczba']]
        except KeyError:
            try:
                return self.root['przymiotnik']['word'][base_word]['stopień'][conf['stopień']]['przypadek'][conf['przypadek']]['liczba'][conf['liczba']]['rodzaj'][conf['rodzaj']]
            except KeyError:
                try:
                    if conf['forma'] == 'czas teraźniejszy':
                        return self.root['czasownik']['word'][base_word]['aspekt'][conf['aspekt']]['forma'][conf['forma']]['liczba'][conf['liczba']]['osoba'][conf['osoba']]
                    else:
                        return self.root['czasownik']['word'][base_word]['aspekt'][conf['aspekt']]['forma'][conf['forma']]['liczba'][conf['liczba']]['osoba'][conf['osoba']]['rodzaj'][conf['rodzaj']]
                except KeyError:
                    raise KeyError("There is no such word in Database")
