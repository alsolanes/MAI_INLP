import subprocess

# Tokenize a file with a list of properties (word, lemma, category of the word, probability assignment). By default considers the input to be in English, but if specified as a parameter can be set to another language like spanish('es')"
def tokenize_file(path_to_file, lang='en'):
    p = subprocess.Popen('analyze -f ' + lang + '.cfg <'+path_to_file+'', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return to_list(p)

# Given an input file, returns a list of words and the type of word it is
def extract_type(path_to_file, lang='en'):
    list_out = tokenize_file(path_to_file, lang)
    res = []
    for a in range(len(list_out[:])):
        if len(list_out[a])>2:
            res.append([list_out[a][0],list_out[a][2]])
    return res

#Given an input file, returns a list of words and the phonetics of the word
def extract_phonetics(path_to_file, lang='en'):
    list_out = subprocess.Popen('analyze -f ' + lang + '.cfg --phon <'+path_to_file+'', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    list_out = to_list(list_out)
    res = []
    for a in range(len(list_out[:])):
        if len(list_out[a])>2:
            res.append([list_out[a][0],list_out[a][1]])
    return res
#Assign probabilities for each analysis of given word
def extract_probabilities(path_to_file, lang='en'):
    list_out = tokenize_file(path_to_file, lang)
    res = []
    for a in range(len(list_out[:])):
        if len(list_out[a])>3:
            res.append([list_out[a][0],list_out[a][3]])
    return res

#Returns a list of names identified by freeling
def get_names(path_to_file, lang='en'):
    list_types = extract_type(path_to_file)
    res = []
    for a in range(len(list_types[:])):
        if list_types[a][1] == 'NP':
            res.append(list_types[a][0])    
    return res
    
# Given an input, returns the output as a structured list.
def to_list(p):
    res = []
    for line in p.stdout.readlines():
            aux = []
            for item in line.split(' '):
                a = item.split('\n')[0]
                if a is not ' ':
                    print 'item ' + a
                    print a is ' '
                    aux.append(a)
            res.append(aux)  
    return res
            
print tokenize_file('input_es.txt')