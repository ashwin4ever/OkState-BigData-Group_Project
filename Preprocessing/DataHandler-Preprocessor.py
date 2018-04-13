import shlex
import sys
from os import listdir
from os.path import isfile, join
import numpy as np
import itertools
#logic to preprocess the raw dataset to a processed data set of user,timestamp and folder accessed
#gives ot a csv on specified path as output.csv
ResFolder = "C:\\Users\\Raj\\Desktop\\GroupProject_Data\\"
onlyfiles = [f for f in listdir ( ResFolder ) if isfile ( join ( ResFolder, f ) )]
from collections import defaultdict, namedtuple
import csv
import re

a = [];
b = [];
dict = {};
mytuple = ();


class DetailsBuilder ( object ):

    def readfile(self,filename):
        with open ( filename, 'rb' ) as inputfile:
            content = inputfile.readlines ()
            content = [x.strip () for x in content]
        return content

    def MyParser(self, filename):
        # search for ip type
        # pattern = re.compile("^\d{1,3}\.d{1,3}\.d{1,3}\.d{1,3}$")
        # Read data from csv format file into a list of namedtuples.
            content = DetailsBuilder().readfile(filename)
            print ( "*******content length" + len ( content ).__str__ () )
            for line in content:
                a.append ( line.__str__ ().split ( ' ' ) )

            for attribs in a:
                if "." in attribs[0].split ( '\'' )[1]:
                    user = attribs[0].split ( '\'' )[1]
                try:
                    Tstamp = attribs[3][1:]
                except:
                    e = sys.exc_info ()[0]
                    Tstamp = ""
                try:
                    splitted = attribs[6].split('/')
                    if (len ( attribs[6].split ( '/' ) ) >=3):
                         Folder = "/"+splitted[1]+"/"+splitted[2]
                    elif(len ( attribs[6].split ( '/' ) ) <3 or len ( attribs[6].split ( '/' ) ) >1):
                        if splitted[1] != "":
                            Folder ="/"+splitted[1]
                        else:
                            Folder = "NA"
                    else:
                        Folder = "NA"
                except:
                    e = sys.exc_info ()[0]
                    if splitted[0] != "" and len(splitted[0]) > 3 :
                        Folder =  splitted[0]
                    else:
                        Folder = "NA"
                   # value = "'User': "+user+", 'timeStamp': "+Tstamp+", 'Folder': "+Folder
                if user in dict.keys():
                     dict[user]['User'] += "~"+user
                     dict[user]['TimeStamp'] += "~"+Tstamp
                     dict[user]['Folder'] += "~"+Folder


                else:
                    dict[user] = {'User':user, 'TimeStamp':Tstamp, 'Folder':Folder}

            return dict


if __name__ == '__main__':
    for f in onlyfiles:

        details = DetailsBuilder ().MyParser ( ResFolder + f )
        i = 0

        ftowrite = open (ResFolder + 'output.csv', 'ab' )

        np.savetxt ( ftowrite,np.column_stack(["Users","TimeStamps","Folders"]), fmt="%s" , delimiter=',' )
        for key, value in sorted ( details.items () ):

            # for valU in value['User'].split ( '~' ):
            #     Valu.append(valU)
            #
            # for valT in value['TimeStamp'].split('~'):
            #     Valt.append(valT)
            # for ValF in value['Folder'].split('~'):
            #     valf.append(ValF)
            for x,y,z in  itertools.zip_longest(value['User'].split ( '~' ),value['TimeStamp'].split('~'),value['Folder'].split('~')):
                i = i + 1
                np.savetxt ( ftowrite, np.column_stack([x,y,z]), delimiter=',', fmt="%s")
    print ( i )
