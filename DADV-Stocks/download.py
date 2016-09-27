'''
Created on Dec 23, 2014

@author: Omair
'''

import errno
import csv
import urllib
import os
# import zipfile
from zipfile import ZipFile
import datetime
from datetime import date
# import solr
import pysolr
url = "http://www.bseindia.com/download/BhavCopy/Equity/" # EQ231214_CSV.ZIP
dir = "data/"

a = date(2013, 1, 1)
b = date(2014, 12, 31)

print "Downloading files between "+a.isoformat()+" and "+b.isoformat()
delta = datetime.timedelta(days=1)  #Date Delta (increment) = 1 day
while a <= b:
    a += delta  #Increase a by one day
    try:
        if a.weekday() < 5: #ignore all weekends
            fileN = "EQ" + a.strftime("%d%m%y") + "_CSV.ZIP"
            zipfilepath = dir+"zips/"+fileN;
            if not os.path.exists(zipfilepath): # If file not already present
                print "Downloading:",a
                urllib.urlretrieve('http://www.bseindia.com/download/BhavCopy/Equity/'+fileN, zipfilepath)
                ffile=open(zipfilepath,'rb')    #open and unzip the CSV inside
                zipping=ZipFile(ffile)
                for name in zipping.namelist():
                    output=dir+"output/"
                    zipping.extract(name,output)
                    ffile.close()
    except:
        continue

print "Files gotten. Extracting CSV files from Zips"
fileDirectory=dir
fileNames=[]
for fileN in os.listdir(fileDirectory+"output/"):
    if fileN.endswith(".CSV"):
        fileNames.append(fileN)
        
# Delete everything from docs        
# http://localhost:8983/solr/collection1/update?stream.body=%3Cdelete%3E%3Cquery%3E*:*%3C/query%3E%3C/delete%3E&commit=true

print "Indexing each file to Solr"
s = pysolr.Solr('http://localhost:8983/solr/collection1')   #Establish conn to Solr

# s.delete(q='*:*') # DELETE ALL records currently indexed 
i = 0
for eachfile in fileNames:
    reader = csv.DictReader(open(dir+"output/"+eachfile,"rb"))
    listOfAllRows = []
    for row in reader:
        row['SC_NAME'] = row['SC_NAME'].strip()
        d = datetime.datetime.strptime( eachfile[2:8], "%d%m%y" )  #Parse date
        row['id'] = str(row['SC_CODE']+d.isoformat()) # creating 'unique' id for each record(document) -> Company Code + Date
        row['DATE'] = str(d.isoformat()+'Z') # formatting date according to Solr format
        listOfAllRows.append(row)
    i = i+ len(listOfAllRows)
    s.add(listOfAllRows)    #Add all rows to Solr index
    print i,eachfile
s.optimize()
print "Indexing finished"

            
            
