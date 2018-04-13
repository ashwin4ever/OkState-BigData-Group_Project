# Hopfield Network to predict patterns


import numpy as np
from neupy import plots
import matplotlib.pyplot as plt
import pandas as pd
import csv
import datetime
from collections import defaultdict
from neupy import algorithms
import scipy.spatial.distance as distance



def calcCosineSimilarity(pat1 , pat2):

      #r , c = mem_pat.shape

      #mp = mem_pat.flatten()
      #tp = test_pat.flatten()

      p1 = pat1.flatten()
      p2 = pat2.flatten()

      #print('Cos: ' , p1 , p2)
       
      cos_sim = 1 - distance.cosine(p1 , p2)

      return cos_sim


def user_process_pattern(user_folder):

      '''

      This function takes in the users and their accessed folders.

      File accessed are excluded from the patterns.

      Returns a dict containing user and folder accessed.
      Returns a list containing the list of folders for all users.

      '''
 
      user_proc_pattern = defaultdict(list)

      folders = []
      tot_folders = []
      #done = False
      
      for key , value in user_folder.items():

            done = False

            for folder in value:
                  
                  # Check for '.' or '?' in folders to get filetype
                  if '.' or '?' in folder:

                        temp = folder

                        while temp.rfind('/') != 0:
                              #print(temp)
                              ridx = temp.rfind('/')
                              if ridx > 0 and len(temp[0 : ridx].strip()) > 3:
                                    temp = temp[0 : ridx]
                                    if '.' or '?' not in temp:
                                          folders.append(temp[0 : ridx].strip())
                                          tot_folders.append(temp[0 : ridx].strip())
                                          break
                              else:
                                    break

                  else:
                        ridx = folder.rfind('/')
                        if len(folder[0 : ridx].strip()) > 3:

                              folders.append(folder[0 : ridx].strip())
                              tot_folders.append(folder[0 : ridx].strip())

            # add to dictionary
            user_proc_pattern[key] = folders
            folders = []

      return user_proc_pattern , tot_folders


def get_unique_folders(folders):

      '''

      This function takes a list of folder accesses and
      returns unique induvidual folders

      '''

      unique_folders = []

      for f in folders:

            for val in f[1 : ].split('/'):
                  
                  if len(val) >= 2:
                        unique_folders.append(val.strip())
                  
      return list(set(unique_folders))


def create_one_hot_encoding(folders):

      '''

      This function takes unique folders as its parameter
      and returns a dictionary containing binary repr of each folder

      '''

      # Make a 1-hot repr
      one_hot_folders = pd.get_dummies(folders , sparse = True)

      # Cast as numpy array
      one_hot_arr = np.array(one_hot_folders)

      # Create a dict to store 1 hot reprs
      one_hot_dict = {}

      for idx , row in enumerate(one_hot_arr):

            if folders[idx] not in one_hot_dict:
                  one_hot_dict[folders[idx]] = row
      

      return one_hot_dict



def generate_user_pattern(user_proc_folder , one_hot_dict):

      '''

      This function generates usage access patterns for
      each of the folders access by the user.

      The function returns a dictionary containing user names
      and trained weight matrices


      '''
      #print([*one_hot_dict.keys()])
      keys = [*one_hot_dict.keys()][0]
      size = len(one_hot_dict[keys])
      pat_str = None

      pat_list = []

      # dict to store binary patterns of folder access
      user_bin_dict = defaultdict(list)

      folder_bin_dict = defaultdict(str)

      
      
      for key , value in user_proc_folder.items():

            for access in value:

                  if '%' not in access and ' ' not in access and 'srqa' not in access:

                        tmp = access[1 : ].split('/')

                        #print(tmp , access , key)

                        if len(tmp) > 1:

                              if '.' not in (tmp[0] and tmp[1]):

                                    pat_str = np.concatenate([one_hot_dict[tmp[0]] , one_hot_dict[tmp[1]]] , axis = 0)
                                    pat_list.append(pat_str)
                                    #print(tuple(pat_str) , access)
                                    folder_bin_dict[tuple(pat_str)] = '/' + tmp[0] + '/' + tmp[1]
                              else:
                                    tmp_arr = np.zeros(size * 2 , dtype = np.int)
                                    tmp_arr[0 : size] = one_hot_dict[tmp[0]]
                                    pat_list.append(tmp_arr)
                                    #print(tuple(tmp_arr) , access)
                                    folder_bin_dict[tuple(tmp_arr)] = '/' + tmp[0]                             
                              
                        
                        else:
                              tmp_arr = np.zeros(size * 2 , dtype = np.int)
                              tmp_arr[0 : size] = one_hot_dict[tmp[0]]
                              pat_list.append(tmp_arr)
                              #print(tuple(tmp_arr) , access)
                              folder_bin_dict[tuple(tmp_arr)] = '/' + tmp[0]


            user_bin_dict[key] = pat_list
            pat_list = []

      return user_bin_dict , folder_bin_dict

if __name__ == '__main__':


      limit = 1891714
      i = 0

      user_time = defaultdict(list)
      user_folder = defaultdict(list)
      time_folder = defaultdict(str)

      time = []
      folder = []
      time_day = []

      user = None
      cur_user = ''
      key = 'user'
      user_idx = 0
      day = None

      '''

      Read from standard input and get the access patterns
      based on timestamp

      '''

      with open('nasa_access_logs.csv') as nasa_csv:
            csv_reader = csv.reader(nasa_csv)

            for row in csv_reader:
                  if i == limit:
                        break
                  elif i > 0 and row[2] != 'NA':

                        cur_user = row[0]
                        cur_day = row[1].split('/')[0]
                        
                        if day is not None and day != cur_day:
                              user_time[key + str(user_idx)] = time
                              user_folder[day] = folder
                              folder = []
                              time = []
                              user_idx += 1
                        
                        else:
                              #print(row)
                              dt = datetime.datetime.strptime(row[1], "%d/%b/%Y:%H:%M:%S")
                              time.append(dt)
                              folder.append(row[2])

                        #user = cur_user
                        day = cur_day

                  # Split time into dd / mm / yyyy
                  # Get the 
                  #time_temp = row[1].split('/')

                  time_folder[row[1]] = row[2]

                  i += 1

      user_folder[day] = folder
      user_proc_folder , tot_folders = user_process_pattern(user_folder)

      # Remove duplicates and get unique list of folders
      unique_comb_folders = list(set(tot_folders))

     
      # Remove foreign symbols
      unique_comb_folders = [f for f in unique_comb_folders if '.' not in f if '%' not in f]

      
      # Get induvidual unique folders
      unique_folders = get_unique_folders(unique_comb_folders)

      # Filter to remove unwanted files missed earlier!!
      unique_folders = [f for f in unique_folders if '.' not in f if '%' not in f]
 

      # Get one hot repr of folders
      # key - folders
      one_hot_dict = create_one_hot_encoding(unique_folders)
      
      # key - time    key - pattern
      user_bin_dict , folder_bin_dict = generate_user_pattern(user_proc_folder , one_hot_dict)

      # Dictionary containing patterns and trained matrices
      pat_hop_net = {}

      sorted_days = sorted(list(user_bin_dict.keys()))

      # Dict to hold the frquently accesed path and its weight value
      d_freq_accessed_path = {}
      d_pattern_count = defaultdict(int)

      test_pat = ''

      dim = 0

      # For each day train the patterns
      for day in sorted_days[0 : 3]:

            file_nm = day + '.txt'

            value = user_bin_dict[day]
            pat_hop_net = {}

            # Get each folder access pattern
            for pat in value:
                  
                  # Create a hopfield network
                  hop_net = algorithms.DiscreteHopfieldNetwork(mode = 'async' , check_limit = False , n_times = 300)

                  # Train the network
                  hop_net.train(pat)

                  # Get the weight matrix
                  hop_wt_mat = hop_net.get_stored_patterns()

                  # Get the dimensions of the matrix
                  dim = hop_wt_mat.shape[0]

                  if tuple(pat) not in pat_hop_net:

                        pat_hop_net[tuple(pat)] = hop_wt_mat

                  else:
                        temp_arr = pat_hop_net[tuple(pat)]
                        wt_sum = np.zeros(temp_arr.shape , dtype = np.int)
                        wt_sum = np.add(temp_arr , hop_wt_mat)
                        np.fill_diagonal(wt_sum , 0)
                        pat_hop_net[tuple(pat)] = wt_sum

            # Print the key - pattern and value - weight_matrix
            print(pat , pat_hop_net[tuple(pat)])
