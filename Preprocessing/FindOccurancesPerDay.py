import numpy as np
from collections import Counter
import re
import pandas as pandas
from neupy import algorithms
import scipy.spatial.distance as distance
from DataHandler import DetailsBuilder
import itertools

#objective Find the occurances for given checklist per day basis
#data set folder
ResFolder = "C:\\Users\\Raj\\Desktop\\GroupProject_Data\\"
myDict={};
mymatrix={};
a = set();
b=set();
valueList =[];
countList =[];
#return the matches between two lists a reusable function
def returnMatches(a, b):
    return [[x for x in a if x in b], [x for x in b if x in a]]
#break down words and filter unnecessary words
def Wordify(a):
    global line
    for line in  list(a) :
        atemp = list ( filter ( None, list (line.split ( '/' ))))
        for s in atemp:
            if not s.isdigit() and ':' not in s :
                if not s.lower() in (('png', 'jpg', 'jpeg','html','http','ftp','www','gif','href')):
                    if len(NormalizeWord(s))>3:
                        aset.add ( NormalizeWord( s ) )
    str_list = list ( filter ( None, list ( aset ) ))
    return str_list
#regex to clean the folder output label
def NormalizeWord(f):
    return re.sub ( r"[^a-zA-Z-_(0-9) ]+", '', f ).strip()

#main logic
if __name__ == '__main__':
    myDict={}
    #reading file
    mydetails = DetailsBuilder().readfile(ResFolder+'nasa_access_logs.csv')
    i=0;
    for line in mydetails:
        if(i!=0):
            currLine = line.__str__().split(',')
            if currLine[1].split(':')[0] in myDict.keys():
                myDict[currLine[1].split ( ':' )[0]]['Date']+="~"+currLine[1].split(':')[0]
                myDict[currLine[1].split ( ':' )[0]]['Folder'] += "~"+currLine[2]
            else:
                #adding full folder structure nad matched folder with date base
                myDict[currLine[1].split(':')[0]] = {'Date':currLine[1].split(':')[0], 'Folder': currLine[2]}

        else:
            i=1


aset = set()
initialKey =0
wordCounter = {}
UserDetails={}
count = 0

#logic to filter for each day
for key, value in  myDict.items ():
    alist = []
    tempb = list(filter(None, value['Folder'].split ( '~' )))
    Checklist = ['resources', 'missions', 'technology', 'apollo', 'soils', 'imagemap','images']
    count =0
    WordFrequency = {}
    for item in tempb:
        for item2 in Checklist:
            if item2 in item:

                    alist.append(item2)

        UserDetails[key] = {'Frequency':WordFrequency,'CountList':alist}

#logic to print per day
for key1,value1 in UserDetails.items():
    tempaa =UserDetails[key1]['CountList']
    countForThiskey = Counter(list(tempaa))
    print ( "***************************************************************" )
    print("the date "+key1+" has  following combination in given checklist")
    print()
    #printing to console
    for n  in countForThiskey.keys():
        print ("the word '"+ n +"' has '"+ countForThiskey[n].__str__() +"'  Occurances")
