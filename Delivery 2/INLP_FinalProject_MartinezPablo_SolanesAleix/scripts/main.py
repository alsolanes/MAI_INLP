# -*- coding: utf-8 -*-
import sys, re
sys.path.insert(0, '../lib')
import xmlToDict_functions as x2d
import dbpedia as dbp
from saveIntoXml_function import *
from scorer import *
'''
A structure class in order to the scorer be able to store data
'''
class structure:
  Qnumber = []
  Query = []
  Local = []
  What = []
  What_type = []
  Geo_relation = []
  Where = []
  Lat_Long = []

'''
Function that reads a file and returns it restructured as a dict
'''
def readXML(File_ds = None):
    if File_ds==None:
        File_ds = "../data/GC_Test_solved_100_2.xml" # solved test data set
    #File_ds = "../data/GC_Test_Not_Solved_100.xml" # test data set
    File_tr = "../data/GC_Tr_100.xml" # training data set
    File_ds_solved = "../data/GC_Test_solved_100_2.xml" # solved test data set
    
    # Load the xml file
    xml_ds = x2d.xmlToDict(File_ds)
    
    #x2d.showQuerieNos()
    #x2d.dumpClean()
    return xml_ds


'''
INPUT: A query in string format
Returns None if it is UNDEFINED
Returns dict(WHAT, WHERE, RELATION) with the correct values found otherwise
'''
def getRelation(query):
    relation_words = "" # the words that can split the sentence
    relation = "UNDEFINED" # the final relation in Upper case
    # CASE SIMPLE
    relations = re.compile(r"\W?\b(?:in|on the|of|near|along the|at|from|to)\b",re.IGNORECASE)
    wrd = relations.findall(query)
    if len(wrd)>0:
        wrd = wrd[0]
        relation_words = wrd
        wrd.replace(" the","")
        wrd = wrd.strip()
        relation = wrd.upper()
    # CASE NEXT TO, IN OR AROUND, IN AND AROUND
    if "next to" in query.lower():
        relation_words = "next to"
        relation = "NEXT_TO"
    elif "in or around" in query.lower():
        relation_words = "in or around"
        relation = "IN_NEAR"
    elif "in and around" in query.lower():
        relation_words = "in and around"
        relation = "IN_NEAR"
        
    # CASE DISTANCE
    relation_km =  re.compile(r"\b(?:within)\W+(?:[0-9]+)\W?(?:miles|m|kilometers|km)\b\W+\b(?:of|to|from)\b", re.IGNORECASE)
    res = relation_km.findall(query)
    if len(res)>0:
        relation = "DISTANCE"
        relation_words = res[0]
        
    # CASE IN THE... OF & SOUTH/WEST... OF/TO
    relation_pos1 = re.compile(r"\W?\b(?:in the)?\b\W?\b(?:south|north|east|west|southeast|southwest|northeast|northwest)+\b\W?\b(?:of|to)+\b", re.IGNORECASE)
    wrd = relation_pos1.findall(query)
    if len(wrd)>0:
        wrd = wrd[0]
        relation_words = wrd
        wrd = wrd.replace("in the ","")
        wrd = wrd.replace("northeast","NORTH_EAST")
        wrd = wrd.replace("southeast","SOUTH_EAST")
        wrd = wrd.replace("northwest","NORTH_WEST")
        wrd = wrd.replace("southwest","SOUTH_WEST")
        wrd = wrd.strip()
        wrd = wrd.replace(" ","_")
        relation = wrd.upper()
    
    if (relation=="UNDEFINED"):
        return {'WHAT':query, 'GEO-RELATION':'Undefined', 'WHERE':''}# if None, non-local query found
    splitted = query.split(relation_words)
    #print "::::::::::::::::Splitted",splitted[1]
    out = {'WHAT':splitted[0].strip(),'GEO-RELATION':relation,'WHERE':splitted[1].strip()}
    return out

'''
given a string, returns if found, the corresponding place.
Input: a string sentence
'''
def getStringLocation(query):
    return dbp.isLocation(query,'en')
    #return dbp2.isLocation(query)
    
'''
Compares two words, if it is not none, it is the same word.
Used for appearances of whole words.
input: a string word
'''
def findWholeWord(w):
    return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search
    
'''
Function that returns the WHAT-TYPE of a sentence.
Input: a string sentence
'''
def getWhatType(what):
    # in order to check the type we consider that if there is no what, it is a map place
    if what=="":
        return 'Map'
    
    # by checking a file that contains words typically in map types we check if it is map
    with open('../lib/map_type_categories.txt','r') as ins:
        for line in ins:
            if line=="\n": continue
            line = line.replace('\n','').lower()
            if findWholeWord(line)(what.lower())!= None:
                #print line, what
                return 'Map'
    # by checking a file that contains words typically in yellow page types we check if it is yellow pages
    with open('../lib/yellow_pages_categories.txt','r') as ins:
        for line in ins:
            if line=="\n": continue
            line = line.replace('\n','').lower()
            if findWholeWord(line)(what.lower())!= None:
                return 'Yellow Page'
    # otherwise the text will be information type
    return 'Information'
    
    
'''
Method that compares two dictionaries, and returns true or false depending if they are equal
In order to compare, it is used the evaluation algorithm explained in the paper.
'''
def evalDicts(dictA, dictB):
    if dictA['WHERE']==None:
        print 'parsed!!!\n\n'
        dictA['WHERE']='None'
    return (dictA['LOCAL']==dictB['LOCAL'] and
            ' '.join(dictA['WHAT'].lower().split())==' '.join(dictB['WHAT'].lower().split()) and
            dictA['WHAT-TYPE']==dictB['WHAT-TYPE'] and dictA['GEO-RELATION']==dictB['GEO-RELATION'] and
            str(dictB['WHERE']).lower().split(',')[0] in str(dictA['WHERE'].lower().split(',')[0]))
#    self.local==golden.local and
#            ' '.join(self.query_what.lower().split())==' '.join(golden.query_what.lower().split()) and
#            self.query_type==golden.query_type and self.geo_relation==golden.geo_relation and
#            str(golden.query_where).lower().split(',')[0] in str(self.query_where).lower().split(',')[0])

    
'''
this function reads the dataset and returns an out.xml set with the results found 
'''
def process_and_save():
    Rep_str = structure()
    # get the list of relation-types
    xml_ds = readXML()
    i = 0
    found = 0
    error = 0
    local = 0
    
    # CORRECTLY DEFINED PROPERTIES
#    correct_what = 0
#    correct_where = 0
#    correct_type = 0
#    correct_local = 0    
#    correct_relation = 0
    
    # iterate over queries
    for q in xml_ds:
        query = xml_ds[q]['QUERY']
        
        out = getRelation(query)
        out['QUERYNO']=q
        out['WHAT-TYPE']=getWhatType(out['WHAT'])
        place = getStringLocation(out['WHERE'])
        # if the where is a place
        if len(place)>0:
            out['WHERE'] = place[0]
            out['LOCAL'] = 'Yes'
        # if where is not a place
        else:
            # in this case can be that there is no geo in text, or that it's not separated by relations
            try:
                place = getStringLocation(query)
                #print "Place found:",place
            except:
                error += 1
                place = None
            if len(place)>0:
                out['WHAT'] = query.replace(place[0].lower(),'')
                out['WHAT'] = out['WHAT'].replace('  ',' ').strip()
                out['WHAT-TYPE']=getWhatType(out['WHAT'])
                if out['WHAT'] == '':
                    out['WHAT'] = 'None'
                    out['WHAT-TYPE'] = 'Map'
                
                out['WHERE'] = place[0]
                out['LOCAL'] = 'Yes'
                out['GEO-RELATION']='None'
            else:
                out['GEO-RELATION']='None'
                out['WHERE'] = 'None'
                out['WHAT'] = 'None'
                out['LOCAL'] = 'No'
                out['WHAT-TYPE'] = 'None'
        
        #print "---"
        #print query
        #print out
        #if xml_ds[q]==out:
#        if evalDicts(out,xml_ds[q]):
#            found += 1
        #else:
            #print "-------------"
            #print query
            #print "GOT:",out
            #print "EXPECT:",xml_ds[q]
        i += 1
#        if out['LOCAL']=='Yes':
#            local += 1
#            #print local
#            
#        if out['WHERE'].lower() in xml_ds[q]['WHERE'].lower():
#            correct_where += 1
#        if out['WHAT'].lower() in xml_ds[q]['WHAT'].lower():
#            correct_what += 1
#        if out['WHAT-TYPE'].lower() in xml_ds[q]['WHAT-TYPE'].lower():
#            correct_type += 1
#        if out['LOCAL'].lower() in xml_ds[q]['LOCAL'].lower():
#            correct_local += 1
#        if out['GEO-RELATION'].lower() in xml_ds[q]['GEO-RELATION'].lower():
#            correct_relation += 1
            
        sys.stdout.write(('='*i)+(''*(100-i))+("\r [ %d"%i+"% ] "))
        sys.stdout.flush()
    
        
        Rep_str.Qnumber.append(q)
        Rep_str.Query.append(query)
        Rep_str.Local.append(out['LOCAL'].strip())
        Rep_str.What.append(out['WHAT'].strip())
        Rep_str.What_type.append(out['WHAT-TYPE'].strip())
        Rep_str.Geo_relation.append(out['GEO-RELATION'].strip())
        Rep_str.Where.append(out['WHERE'].strip())
        Rep_str.Lat_Long.append('')
    saveIntoXml(Rep_str)
#    print "\NWhat:",correct_what
#    print "Where:",correct_where
#    print "What-type:",correct_type
#    print "Relation:",correct_relation
#    print "Local:",correct_local

'''
main method
'''
def main():
    print "INLP - GeoCLEF2007 Project"
    print "Students: Pablo Martinez and Aleix Solanes"
    print "\nMENU"
    print "1.- Execute code with GC_Test_solved_100_2.xml (process and save xml)"
    print "2.- Show the results of the OutFile.xml"
    opt = input("Select the option you desire:")
    if opt==1:
        process_and_save()
    elif opt == 2:
        
        queries = parser("../scripts/OutFile.xml")
        goldens = parser("../data/GC_Test_solved_100_2.xml")
        unsorted = True
        usepaper = False
        
        results = obtain_score(queries, goldens, unsorted, usepaper)
        print "\nPaper formulas:"
        print "\nPrecision:", results[0]
        print "Recall:", results[1]
        print "F1-Score:", results[2]
        
        usepaper = True
        results = obtain_score(queries, goldens, unsorted, usepaper)
        print "\n\nNormal formulas:"
        print "\nPrecision:", results[0]
        print "Recall:", results[1]
        print "F1-Score:", results[2]

main()