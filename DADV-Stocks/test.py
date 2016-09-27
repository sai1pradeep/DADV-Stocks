'''
Created on Dec 23, 2014

@author: Omair
'''
import os
import csv


fileDirectory= "D:/OneDrive/Workspace/DataVisualization/exam1data/"
fileNames=[]
print "hello"
for fileN in os.listdir(fileDirectory):
    if fileN.endswith(".csv"):
        fileNames.append(fileN)

readerobjects = []
for eachFile in fileNames:
    print eachFile
    readerobjects.append(csv.reader(open(fileDirectory+eachFile,"rb")))

for onefile in readerobjects:
    print onefile.next()
    print "------"
