import numpy as np
from collections import Counter
import re
import pandas as pandas
from neupy import algorithms
import scipy.spatial.distance as distance
from DataHandler import DetailsBuilder
import itertools

#objective is to know for the given checklist .to get patters matching to chicklist for each day in the preprocessed dataset(for faster processing)

#Setting dataset folder (change this as needed)
ResFolder = "C:\\Users\\Raj\\Desktop\\GroupProject_Data\\"
#initializing Variables
myDict={};
mymatrix={};
a = set();
b=set();
valueList =[];
countList =[];

def returnMatches(a, b):
    return [[x for x in a if x in b], [x for x in b if x in a]]
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
def NormalizeWord(f):
    return re.sub ( r"[^a-zA-Z-_(0-9) ]+", '', f ).strip()
#main Logic begins here
if __name__ == '__main__':
    #read the particular processed data csv
    mydetails = DetailsBuilder().readfile(ResFolder+'nasa_access_logs.csv')
    i=0;
    for line in mydetails:
        if(i!=0):
            currLine = line.__str__().split(',')
            if currLine[0] in myDict.keys ():
                myDict[currLine[0]]['User'] += "~" + currLine[0]
                if ':' in currLine[1]:
                    vr1 = list(filter(None,currLine[1].split(':')))
                    myDict[currLine[0]]['Date'] += "~" + vr1[0]
                if '.' in currLine[2]:
                    try:
                        vr = list(filter(None,currLine[2].split('/')))
                        myDict[currLine[0]]['Folder'] += "~" + vr[0]
                        if  '.' in vr[0] or 'NA' in vr[0] or '?' in vr[0] or ' ' in vr[0]:
                             print()
                        else:
                            if not currLine[2].isdigit():
                                a.add ( vr[0] )

                    except:
                        print(vr)
                else:
                    myDict[currLine[0]]['Folder'] += "~" + currLine[2]
                    if 'NA' not in currLine[2] and '?' not in currLine[2] and not currLine[2].isdigit() and ' ' not in currLine[2] :
                        a.add ( currLine[2] )


            else:
                myDict[currLine[0]] = {'User': currLine[0],'Date':currLine[1].split(':')[0], 'Folder': currLine[2]}
            b.add ( currLine[2] )
            i+=1
        else:
            i+=1
aset = set()
initialKey =0
wordCounter = {}
UserDetails={}
count = 0
for key, value in  myDict.items ():
    #getting date for each user to reduce the logic on date basis
    tempa = list(filter(None,value['Date'].split('~')))
    tempb = list(filter(lambda k: 'NA' not in k, value['Folder'].split ( '~' )))
    Checklist = ['resources', 'missions', 'technology', 'apollo', 'soils', 'imagemap']
    FullFolderList =[]
    MatchedFolder =[]
    for date,fullfolder in itertools.zip_longest(tempa,tempb):
        for item in Checklist:
            try:
                if item in fullfolder and fullfolder != None:
                    if date in wordCounter.keys():
                        wordCounter[date]['Rawpath'] += "~"+fullfolder
                        wordCounter[date]['checklistItem'] += "~"+item
                    else:
                        #getting the fullpath and matched checlist path fro the particular date
                        wordCounter[date]={'Rawpath':fullfolder,'checklistItem':item}
            except:
                print()
    wordTempCounter = wordCounter.copy()
    UserDetails[key] =wordTempCounter
    wordTempCounter = {}
for key1 in wordCounter.keys():
    tempmainfolder = wordCounter[key1]['Rawpath'].split('~')
    tempmatched =  wordCounter[key1]['checklistItem'].split('~')
    print(tempmainfolder)
    print ( tempmatched )
