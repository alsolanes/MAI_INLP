# -*- coding: utf-8 -*-

import sys
sys.path.insert(0, '../lib')
import xmlToDict_functions as x2d

'''
Usage example
'''
FILE_ds = "../data/GC_10.xml" # data set
FILE_tr = '../data/GC_Tr_100.xml' # training data set

Q_ID  = 5017
Q_ATT = 'LAT-LONG'

# Load & parse xml file
xmldict = x2d.xmlToDict(FILE_tr)

# Ordered string representation
x2d.showQuerieNos()
x2d.dumpClean()

# 2 equivalent ways to reperesent a QUERY
x2d.dumpClean(Q_ID)
x2d.dumpCleanItem(Q_ID)

# You can directly access elements and values like this:
xmldict[Q_ID][Q_ATT], xmldict[Q_ID]
