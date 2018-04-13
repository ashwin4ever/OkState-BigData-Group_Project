import numpy as np
from collections import Counter
import re
import pandas as pandas
from neupy import algorithms
import scipy.spatial.distance as distance
from DataHandler import DetailsBuilder
import itertools



ResFolder = "C:\\Users\\Raj\\Desktop\\GroupProject_Data\\"
myDict={};
mymatrix={};
a = set();
b=set();
valueList =[];
countList =[];

def calcCosineSimilarity(mem_pat, test_pat):
    r, c = mem_pat.shape

    mp = mem_pat.flatten ()
    tp = test_pat.flatten ()

    # print(mp)
    # print(tp)

    cos_sim = 1 - distance.cosine ( mp, tp )

    # print(jaccard_similarity_score(mp , tp))
    return cos_sim

def zerolistmaker(n):
    listofzeros = [0] * n
    return listofzeros
def indices_to_one_hot(data, nb_classes):
    """Convert an iterable of indices to one-hot encoded labels."""
    targets = np.array(data).reshape(-1)
    return np.eye(nb_classes)[targets]

if __name__ == '__main__':
    mydetails = DetailsBuilder().readfile(ResFolder+'output.csv')
    i=0;
    for line in mydetails:
        if(i!=0):
            currLine = line.__str__().split(',')
            if currLine[0] in myDict.keys ():
                myDict[currLine[0]]['User'] += "~" + currLine[0]
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
                myDict[currLine[0]] = {'User': currLine[0], 'Folder': currLine[2]}
            b.add ( currLine[2] )
            i+=1
        else:
            i+=1
initialKey = "";
tempListrow=[];
CopyWithfrequencyCount={};
tempListcol = [];
Matrix = np.zeros ( [len ( a ), len ( a )], dtype=int )
for f in a.__iter__ ():
    tempListrow.append ( f )
tempListcol = tempListrow


def IntitalImplementation():
    global i
    # tomake sure that every key follows same n attributes rule
    for i in range ( 0, len ( tempListrow ) ):
        for j in range ( 0, len ( tempListcol ) ):
            tempa = tempListcol[j]
            tempb = CopyWithfrequencyCount[tempa]
            count = 0
            if tempb != 0:
                Matrix[i][j] = tempb
                Matrix[j][i] = tempb
                CopyWithfrequencyCount.pop ( tempa, None )

        # matrix is already with zero so not explicitly need to set zeros again
    return Matrix

def NewImplementation():
    global i
    # tomake sure that every key follows same n attributes rule
    for i in range ( 0, len ( tempListrow ) ):
        for j in range ( 0, len ( tempListcol ) ):
            tempa = tempListcol[j]
            tempb = CopyWithfrequencyCount[tempa]
            count = 0
            if tempb != 0:
                Matrix[i][j] = tempb
                Matrix[j][i] = tempb
                #CopyWithfrequencyCount.pop ( tempa, None )

        # matrix is already with zero so not explicitly need to set zeros again
    return Matrix
aset=set()

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
hopfield_net = algorithms.DiscreteHopfieldNetwork ( mode='async', n_times=200,check_limit=False)
for key in myDict.keys():
    arb = []
    if key!=initialKey:
        initialKey = key
        stra = myDict[key]['Folder'].split('~')
        sf = pandas.get_dummies(Wordify (a))
        #sf= pandas.get_dummies(['images' , 'shuttle',  'resources' , 'apollo' , 'history'])
        print(list(sf._info_axis._data))
        ara = np.array(sf)
        BinaryFolder = {}
        WithFolderFrequencyCount = Counter ( stra )
        # CopyWithfrequencyCount = WithFolderFrequencyCount.copy ()
        for i,axis in itertools.zip_longest(range(0,len(ara)),reversed(list ( filter ( None, list ( sf.columns.values ) ) ))):
            BinaryFolder[axis] = {'FolderRep': ara[i]}
            #np.concatenate((np.zeros(len(ara[i])),ara[i]),axis=0)
            arb.append(np.concatenate((np.zeros(len(ara[i])),ara[i]),axis=0))
        combinedMat = ara
        # for k,l,key1 in itertools.zip_longest(range(0,len(BinaryFolder.keys())),range(len ( Wordify (a) )),BinaryFolder.keys()):
        #     Match = [word for word in stra if key1 in word]
        #     if len(Match) >1 :
        #         for m in Match:
        #             an = list(filter(None,m.split("/")))
        #             try:
        #                 if len(an)>1 and len(an[1])>2:
        #                     combinedMat[k] = BinaryFolder[NormalizeWord(an[0])]['FolderRep'] + BinaryFolder[NormalizeWord(an[1])]['FolderRep']
        #                     combinedMat[l][k] = combinedMat[k][l]
        #                 else:
        #                     combinedMat[k] = BinaryFolder[NormalizeWord ( an[0] )]['FolderRep']
        #                     combinedMat[l][k] = combinedMat[k][l]
        #             except:
        #                 print ( an )
    # to normalize values supportd by hopfied either 0 /1
    #combinedMat[combinedMat > 1] = 1
    patterns =  ['/images/shuttle' , '/history/shuttle' , '/history/shuttle' , '/images/shuttle']
    mymatrix[key] = {'User': key, 'Combined': combinedMat, "VisitedFolderWithFrequency": WithFolderFrequencyCount,
                     'BinaryRepresentation': BinaryFolder}
    #individual hot word folders matrix to train
    hopfield_net.train ( np.array(arb) )
    #training combined folder pattern manually /shuttle/technology
    shuttle = np.array(BinaryFolder['shuttle']['FolderRep'])
    history = np.array(BinaryFolder['history']['FolderRep'])
    images = np.array ( BinaryFolder['images']['FolderRep'] )
    #comining /shuttle and /Technology pattern
    aa=np.concatenate((images,shuttle),axis=0)
    aa1 = np.concatenate ( (history,shuttle), axis=0 )
    aa2=np.concatenate((BinaryFolder['images']['FolderRep'],shuttle),axis=0)
    aa3 = np.concatenate ( (BinaryFolder['history']['FolderRep'], shuttle), axis=0 )
    getter_values = hopfield_net.get_Weight
    hopfield_net.set_Weight = np.array([aa,aa1,aa2,aa3])
    hopfield_net.train(np.matrix([aa,aa1,aa2,aa3]))
    # hopfield_net.train ( aa1 )
    # hopfield_net.train ( aa2 )
    # hopfield_net.train ( aa3 )
    prediction = hopfield_net.predict(np.concatenate((np.zeros(len(shuttle)),shuttle),axis=0))
    cs = calcCosineSimilarity(prediction,np.concatenate((np.zeros(len(shuttle)),shuttle),axis=0))
    print(cs)
#     break
#
#     #print ( '\n'.join ( [''.join ( ['{:4}'.format ( item ) for item in row] ) for row in combinedMat] ) )
#
#
# patterns = ['/cgi-bin/imagemap','/shuttle/technology', '/shuttle/missions', '/shuttle/countdown']
#
# asas =[]
# for k,s in (mymatrix.items()):
#     asas.append(s['Combined'])
#
#     data = asas[0]
#     hopfield_net.train ( data )
#     ss = hopfield_net.get_Weight
#
#     hopfield_net.train (data)
#     noise_two = np.rot90 ( np.matrix ( np.copy ( patterns ) ) )
#     result = hopfield_net.predict(noise_two)
#     print(result)
