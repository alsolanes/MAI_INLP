
from SPARQLWrapper import SPARQLWrapper, JSON
import re
import sys

def evaluation():
    locs = loadInstances(workingDir+'locs')
    ok = 0
    ko = 0
    for c in locs:
        for t in locs[c]:
            try:
                loc = isLocation(t,'en')
                print t, loc
                if loc:
                    ok+=1
                else:
                    ko+=1
            except:
                pass
    print ok,ko, float(ok)/(ok+ko)

def isLocation (term, lang):

    global sparql
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")

    if lang == 'en':
        query ="""
            PREFIX yago: <http://dbpedia.org/class/yago/>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX res: <http://dbpedia.org/resource/>
            ASK  WHERE {
                { res:**1** rdf:type <http://www.ontologydesignpatterns.org/ont/d0.owl#Location>}
                UNION
                { res:**1** rdf:type <http://dbpedia.org/ontology/Place>}
                UNION
                { res:**1** rdf:type <http://dbpedia.org/ontology/PopulatedPlace>}
                UNION
                { res:**1** rdf:type <http://umbel.org/umbel/rc/PopulatedPlace>}
                UNION
                { res:**1** rdf:type <http://schema.org/Place>}
                UNION
                { res:**1** rdf:type <http://dbpedia.org/class/yago/YagoGeoEntity>} .
            }
        """
    elif lang == 'es':
        query ="""
            PREFIX yago: <http://dbpedia.org/class/yago/>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX res: <http://es.dbpedia.org/resource/>
            ASK  WHERE {
                { res:**1** rdf:type <http://www.ontologydesignpatterns.org/ont/d0.owl#Location>}
                UNION
                { res:**1** rdf:type <http://dbpedia.org/ontology/Place>}
                UNION
                { res:**1** rdf:type <http://dbpedia.org/ontology/PopulatedPlace>}
                UNION
                { res:**1** rdf:type <http://umbel.org/umbel/rc/PopulatedPlace>}
                UNION
                { res:**1** rdf:type <http://schema.org/Place>}
                UNION
                { res:**1** rdf:type <http://dbpedia.org/class/yago/YagoGeoEntity>} .
            }
        """
    elif lang == 'fr':
        query ="""
            PREFIX yago: <http://dbpedia.org/class/yago/>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX res: <http://fr.dbpedia.org/resource/>
            ASK  WHERE {
                { res:**1** rdf:type <http://www.ontologydesignpatterns.org/ont/d0.owl#Location>}
                UNION
                { res:**1** rdf:type <http://dbpedia.org/ontology/Place>}
                UNION
                { res:**1** rdf:type <http://dbpedia.org/ontology/PopulatedPlace>}
                UNION
                { res:**1** rdf:type <http://umbel.org/umbel/rc/PopulatedPlace>}
                UNION
                { res:**1** rdf:type <http://schema.org/Place>}
                UNION
                { res:**1** rdf:type <http://dbpedia.org/class/yago/YagoGeoEntity>} .
            }
        """
    wordGroups = splitText(term)
    tempQuery = query
    listWords = []
    for x in range(0, len(wordGroups)):
        word = wordGroups[x].replace(' ','_')
        query = query.replace('**1**', word)
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        results = sparql.query()
        rta = results.convert()
        result = rta['boolean']
        if result:
            listWords.append(wordGroups[x])
        query = tempQuery
         
    return listWords;


def isCity (term, lang):

    global sparql
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")

    if lang == 'en':
        query ="""
            PREFIX yago: <http://dbpedia.org/class/yago/>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX res: <http://dbpedia.org/resource/>
            ASK  WHERE {
                { res:**1** rdf:type <http://dbpedia.org/ontology/Settlement>}
                UNION
                { res:**1** rdf:type <http://umbel.org/umbel/rc/City>}
                UNION
                { res:**1** rdf:type <http://umbel.org/umbel/rc/Village>} .
            }
        """
    elif lang == 'es':
        query ="""
            PREFIX yago: <http://dbpedia.org/class/yago/>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX res: <http://es.dbpedia.org/resource/>
            ASK  WHERE {
                { res:**1** rdf:type <http://dbpedia.org/ontology/Settlement>}
                UNION
                { res:**1** rdf:type <http://umbel.org/umbel/rc/City>}
                UNION
                { res:**1** rdf:type <http://umbel.org/umbel/rc/Village>} .
            }
        """
    elif lang == 'fr':
        query ="""
            PREFIX yago: <http://dbpedia.org/class/yago/>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX res: <http://fr.dbpedia.org/resource/>
            ASK  WHERE {
                { res:**1** rdf:type <http://dbpedia.org/ontology/Settlement>}
                UNION
                { res:**1** rdf:type <http://umbel.org/umbel/rc/City>}
                UNION
                { res:**1** rdf:type <http://umbel.org/umbel/rc/Village>} .
            }
        """
    
    wordGroups = splitText(term)
    tempQuery = query
    listWords = []
    for x in range(0, len(wordGroups)):
        word = wordGroups[x].replace(' ','_')
        query = query.replace('**1**', word)
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        results = sparql.query()
        rta = results.convert()
        result = rta['boolean']
        if result:
            listWords.append(wordGroups[x])
        query = tempQuery
         
    return listWords;


def isState (term, lang):

    global sparql
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")

    if lang == 'en':
        query ="""
            PREFIX yago: <http://dbpedia.org/class/yago/>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX res: <http://dbpedia.org/resource/>
            ASK  WHERE {
                { res:**1** rdf:type <http://dbpedia.org/class/yago/StatesOfTheUnitedStates>}.
            }
        """
    elif lang == 'es':
        query ="""
            PREFIX yago: <http://dbpedia.org/class/yago/>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX res: <http://es.dbpedia.org/resource/>
            ASK  WHERE {
                { res:**1** rdf:type <http://dbpedia.org/class/yago/StatesOfTheUnitedStates>}.
            }
        """
    elif lang == 'fr':
        query ="""
            PREFIX yago: <http://dbpedia.org/class/yago/>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX res: <http://fr.dbpedia.org/resource/>
            ASK  WHERE {
                { res:**1** rdf:type <http://dbpedia.org/class/yago/StatesOfTheUnitedStates>}.
            }
        """
    
    wordGroups = splitText(term)
    tempQuery = query
    listWords = []
    for x in range(0, len(wordGroups)):
        word = wordGroups[x].replace(' ','_')
        query = query.replace('**1**', word)
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        results = sparql.query()
        rta = results.convert()
        result = rta['boolean']
        if result:
            listWords.append(wordGroups[x])
        query = tempQuery
         
    return listWords;

def isCountry (term, lang):

    global sparql
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")

    if lang == 'en':
        query ="""
            PREFIX yago: <http://dbpedia.org/class/yago/>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX res: <http://dbpedia.org/resource/>
            ASK  WHERE {
                { res:**1** rdf:type <http://dbpedia.org/ontology/Country>}
                UNION
                { res:**1** rdf:type <http://umbel.org/umbel/rc/Country>}
            }
        """
    elif lang == 'es':
        query ="""
            PREFIX yago: <http://dbpedia.org/class/yago/>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX res: <http://es.dbpedia.org/resource/>
            ASK  WHERE {
                { res:**1** rdf:type <http://dbpedia.org/ontology/Country>}
                UNION
                { res:**1** rdf:type <http://umbel.org/umbel/rc/County>}
             }
        """
    elif lang == 'fr':
        query ="""
            PREFIX yago: <http://dbpedia.org/class/yago/>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX res: <http://fr.dbpedia.org/resource/>
            ASK  WHERE {
                { res:**1** rdf:type <http://dbpedia.org/ontology/Country>}
                UNION
                { res:**1** rdf:type <http://umbel.org/umbel/rc/County>}
             }
        """
    
    wordGroups = splitText(term)
    tempQuery = query
    listWords = []
    for x in range(0, len(wordGroups)):
        word = wordGroups[x].replace(' ','_')
        query = query.replace('**1**', word)
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        results = sparql.query()
        rta = results.convert()
        result = rta['boolean']
        if result:
            listWords.append(wordGroups[x])
        query = tempQuery
         
    return listWords;

def isRegion (term, lang):

    global sparql
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")

    if lang == 'en':
        query ="""
            PREFIX yago: <http://dbpedia.org/class/yago/>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX res: <http://dbpedia.org/resource/>
            ASK  WHERE {
                { res:**1** rdf:type <http://dbpedia.org/ontology/Region>}
                UNION
                { res:**1** rdf:type <http://umbel.org/umbel/rc/GeographicalRegion>}
            }
        """
    elif lang == 'es':
        query ="""
            PREFIX yago: <http://dbpedia.org/class/yago/>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX res: <http://es.dbpedia.org/resource/>
            ASK  WHERE {
                { res:**1** rdf:type <http://dbpedia.org/ontology/Region>}
                UNION
                { res:**1** rdf:type <http://umbel.org/umbel/rc/GeographicalRegion>}
             }
        """
    elif lang == 'fr':
        query ="""
            PREFIX yago: <http://dbpedia.org/class/yago/>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX res: <http://fr.dbpedia.org/resource/>
            ASK  WHERE {
                { res:**1** rdf:type <http://dbpedia.org/ontology/Region>}
                UNION
                { res:**1** rdf:type <http://umbel.org/umbel/rc/GeographicalRegion>}
             }
        """    
   
    wordGroups = splitText(term)
    tempQuery = query
    listWords = []
    for x in range(0, len(wordGroups)):
        word = wordGroups[x].replace(' ','_')
        query = query.replace('**1**', word)
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        results = sparql.query()
        rta = results.convert()
        result = rta['boolean']
        if result:
            listWords.append(wordGroups[x])
        query = tempQuery
         
    return listWords;


def splitText(text):

    text = re.sub(r'[,\s]+', '_', text)
    listWords = []
    if text <> '' and text <> '_':
        words = text.split('_')
        temp = len(words)
        remaining = ''
        if temp <> 0:
            for x in range(0, len(words)):
                word = ''
                for y in range(0, temp):
                    word = word + words[y]
                    if y <> temp - 1:
                        word = word + ' '
                listWords.append(word.title())    
                temp = temp - 1
                if x <> 0:
                    remaining = remaining + words[x] + ' '
            listWords = listWords + splitText(remaining.strip())        

    return listWords;        



