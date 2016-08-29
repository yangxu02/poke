#!/usr/bin/python

from scrape import *
import inspect
import os
import pickle

class Pokemon:
    def __init__(self, attr_names, attr_vals):
        self.attr_names = attr_names
        self.attr_vals = attr_vals

    def to_str(self):
        #attributes = inspect.getmembers(Pokemon, lambda a:not(inspect.isroutine(a)))
        #attrs = [a for a in attributes if not(a[0].startswith('__') and a[0].endswith('__'))]
        print self.__dict__

LIST_URL = 'http://pokemondb.net/spinoff/go/pokedex'
POKEMON_URL = 'http://pokemondb.net/pokedex/%s'
TYPE_URL = 'http://pokemondb.net/type/%s'
MOVIE_URL = 'http://pokemondb.net/move/%s'

def get_url(url_base, ident):
    return url_base % (ident.replace(' ', '-').lower())

doc = None
if os.path.exists('tmp'):
    with open('tmp', 'rb') as fp:
        doc = pickle.load(fp)

if doc is None:
    s.go('http://pokemondb.net/spinoff/go/pokedex')
    #print s.headers
    doc = s.doc
    with open('tmp', 'wb') as fp:
        pickle.dump(doc, fp)


table = doc.first('table')
head = table.first('thead')
headers =  head.text.encode('utf-8').split('\n')

print headers

body = table.first('tbody')
rows = body.all(tagname = 'tr')
pokemons = []
pokemon_dict = []
dict_keys = ["id" , "name", "type", "stamina", "attack", "defense", "capture_rate", "flee_rate", "candy", "quick_moves", "special_moves"]
dict_key_types = ["int" , "str", "list", "int", "int", "int", "%", "%", "int", "list", "list"]
for row in rows:
    cols = row.all(tagname = 'td')
    vals = []
    pokemon_text = {}
    i = 0
    for col in cols:
        vals.append(col.text.encode('utf-8').replace('\xe2\x80\x94', '-').split('\n'))
        text = col.text.encode('utf-8').replace('\xe2\x80\x94', '-');
        if dict_key_types[i] == 'list':
            pokemon_text[dict_keys[i]] = text.split('\n')
        elif dict_key_types[i] == 'int':
            pokemon_text[dict_keys[i]] = -1 if '-' == text else int(text)
        elif dict_key_types[i] == '%':
            pokemon_text[dict_keys[i]] = -1 if '-' == text else float(text[:-1]) / 100
        elif dict_key_types[i] == 'str':
            pokemon_text[dict_keys[i]] = text

        i += 1
    pokemon_dict.append(pokemon_text)
    pokemons.append(Pokemon(headers, vals))
    print str(headers) + " = " + str(vals)

with open("pokemon.json", 'wb') as fp:
    fp.write(str(pokemon_dict))

with open('pokemon_list', 'wb') as fp:
    pickle.dump(pokemons, fp)


