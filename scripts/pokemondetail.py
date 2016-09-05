#!/usr/bin/python

from scrape import *
import inspect
import os
import pickle
import sys

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

BASIC_LI_ID = 'svtabs_basic_1'


def get_url(url_base, ident):
    return url_base % (ident.replace(' ', '-').lower())

def all_named_div(div, i, results):
    if i == 5:
        return
    subdivs = div.all(tagname = 'div')
    if subdivs is None or len(subdivs) == 0:
        h2s = div.all(tagname = 'h2')
        if h2s is None or len(h2s) == 0:
            return
        else:
            results.append(div)
    else:
        for subdiv in div.all(tagname = 'div'):
            all_named_div(subdiv, i + 1, results)

def getDataInTds(td):
    vals = []
    vals.append(td.text.encode('utf-8'))

def parseDex(div):
    dex = {}
    trs = div.all(tagname = 'tr')
    for tr in trs:
        th = tr.first('th').text.encode('utf-8')
        tag = th.lower()
        val = tr.text.encode('utf-8')[len(th):].strip(' ')
        if 'national' in tag:
            dex['national'] = val
        elif 'type' == tag:
            dex['type'] = val
        elif 'species' == tag:
            dex['species'] = val
        elif 'height' == tag:
            dex['height'] = val
        elif 'weight' == tag:
            dex['weight'] = val
        elif 'abilities' == tag:
            dex['abilities'] = val
        elif 'local' in tag:
            dex['local'] = val
        elif 'japanese' == tag:
            dex['japanese'] = val

    return dex


doc = None
if os.path.exists('tmp_detail'):
    with open('tmp_detail', 'rb') as fp:
        doc = pickle.load(fp)

if doc is None:
    s.go('http://pokemondb.net/pokedex/bulbasaur')
    #print s.headers
    doc = s.doc
    with open('tmp_detail', 'wb') as fp:
        pickle.dump(doc, fp)


lis = doc.all(tagname = 'li')
named_divs = []
for li in lis:
    if 'id' in li.attrs and BASIC_LI_ID == li.attrs['id']:
        divs = li.all(tagname = 'div')
        i = 0
        results = []
        for div in divs:
            all_named_div(div, 0, results)

        for div in results:
            header = div.first('h2').text.encode('utf-8').lower()
            #print div.text.encode('utf-8')
            if 'pok' in header and 'dex data' in header:
                dex = parseDex(div)
                print str(dex)

            

        #print li.text.encode('utf-8')

sys.exit(0)
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


