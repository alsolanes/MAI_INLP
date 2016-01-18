#Luis Alberto Garza Elizondo
#Update: 20/Sept/2015
#Natural Languaje Processing Project.

def saveIntoXml(Rep_str):
  '''Save a structure(Rep_str) with some attributes, into a file(OutFile) with XML format. 
  Rep_str has to be a class with attributes 

    Rep_str.Qnumber
    Rep_str.Query
    Rep_str.Local
    Rep_str.What
    Rep_str.What_type
    Rep_str.Geo_relation
    Rep_str.Where
    Rep_str.Lat_Long  '''

  infile = open('OutFile.xml', 'w')
  infile.write('<OUTPUT-FILE>' + '\n')
  infile.close()

  infile = open('OutFile.xml', 'a')
  for list in range(len(Rep_str.Qnumber)):
    infile.write('<QUERYNO>' + str(Rep_str.Qnumber[list]) + '</QUERYNO>' + '\n')
    infile.write('<QUERY>' + str(Rep_str.Query[list]) + '</QUERY>' + '\n')
    infile.write('<LOCAL>' + str(Rep_str.Local[list]) + '</LOCAL>' + '\n')
    infile.write('<WHAT>' + str(Rep_str.What[list]) + '</WHAT>' + '\n')
    infile.write('<WHAT-TYPE>' + str(Rep_str.What_type[list]) + '</WHAT-TYPE>' + '\n')
    infile.write('<GEO-RELATION>' + str(Rep_str.Geo_relation[list]) + '</GEO-RELATION>' + '\n')
    infile.write('<WHERE>' + str(Rep_str.Where[list]) + '</WHERE>' + '\n')
    infile.write('<LAT-LONG>' + str(Rep_str.Lat_Long[list]) + '</LAT-LONG>' + '\n')

  infile.write('</OUTPUT-FILE>')
  infile.close()


