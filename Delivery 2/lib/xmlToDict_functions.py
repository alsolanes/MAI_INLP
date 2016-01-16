# -*- coding: utf-8 -*-

try:
    from xml.etree import ElementTree
except:
    from elementtree import ElementTree

class AutoVivification(dict):
    """
    Implementation of perl's autovivification feature.
    Used as a properly way to initialize a dict of dicts in Python.
    """
    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            value = self[item] = type(self)()
            return value
###############################################################################
            
global d
d = AutoVivification()

'''
XML format:
-----------
<EXAMPLE-SET>

    <QUERYNO>id</QUERYNO>
        <QUERY>value</QUERY>
        <LOCAL>value</LOCAL>
        <WHAT>value</WHAT>
        <WHAT-TYPE>value</WHAT-TYPE>
        <GEO-RELATION>value</GEO-RELATION>
        <WHERE>value</WHERE>
        <LAT-LONG>value</LAT-LONG>
        
     <QUERYNO>id</QUERYNO>
         (...)
'''
def xmlToDict(filename):
    """
    Python function that makes working with XML feel like you are working with JSON
    """
    assert isinstance(filename, str), "Input variable should be a filename string"
    
    tree = ElementTree.parse(filename)
    root = tree.getroot()
    
    for i in range(len(root)):
        if root[i].tag=='QUERYNO':
            id = int(root[i].text)
            d[id]
        else:
            d[id][root[i].tag] = root[i].text
    return d


def showQuerieNos():
    """
    Prints a formatted representation of all the QUERY Nos registered in the
    dictionary.
    """
    print( len(d.keys()), "QUERIES REGISTERED:\n" +
          "-----------------------\n" +
          ', '.join(map(str, sorted(d.keys())) ))

def dumpCleanItem(i):
    """
    Generates a properly formatted dump for a certain entry 'i' from the dictionary 
    """
    assert i in d.keys(), "Not a valid QUERY id"
    print('\nQUERY '+str(i) + ': ' + d[i]['QUERY'])
    print '\n'.join(['\t'+y+': '+str(d[i][y]) for y in d[i] if y!='QUERY'])
    
def dumpClean(id=None):
    """
    Generates a complete dumping if no paramater is given.
    If 'id' is specified, only that element will be dumped.
    """
    assert isinstance(d, dict), "Input variable is not a dictionary."
    if id is not None:
        dumpCleanItem(id)
    else:
        [dumpCleanItem(x) for x in sorted(d)]

