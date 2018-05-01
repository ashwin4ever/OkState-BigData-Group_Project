'''

Reducer job which accumulates the pattern: key and the
corresponding weight matrices as values.

based on the result of the function calc_similar_patterns
the weight matrices are augmented


'''



import argparse as ap
import numpy as np
from neupy import plots
import matplotlib.pyplot as plt
import pandas as pd
import csv
import datetime
from collections import defaultdict
import nasa_right_mapper as rm
from neupy import algorithms
import scipy.spatial.distance as distance



def calc_similar_patterns(pat_hop_net , folder_bin_dict):

      keys = pat_hop_net.keys()

      keys = [np.array(k) for k in keys]

      #print([*folder_bin_dict.keys()])

      for i in range(0 , len(keys)):

            for j in range(i + 1 , len(keys)):

                  cos_sim = calcCosineSimilarity(keys[i] , keys[j])

                  #print(keys[i] , keys[j])

                  #print('Similarity between ' , folder_bin_dict[tuple(keys[i])] , 'and ',
                          #folder_bin_dict[tuple(keys[j])], ' is ' , cos_sim)

                  if cos_sim > 0.48:

                        #print('Augmenting patterns: ' , folder_bin_dict[tuple(keys[i])] , folder_bin_dict[tuple(keys[j])])
                        arr1 = pat_hop_net[tuple(keys[i])]
                        arr2 = pat_hop_net[tuple(keys[j])]

                        wt_comb = np.zeros(arr1.shape , dtype = np.int)

                        wt_comb = np.add(arr1 , arr2)
                        np.fill_diagonal(wt_comb , 0)

                        #pat_hop_net[tuple(keys[i])] = wt_comb
                        pat_hop_net[tuple(keys[j])] = wt_comb
                        



def generate_test_bin_pattern(pattern , one_hot_dict):

      '''

      This function generates a binary pattern for test cases

      '''

      pat = pattern[1 : ].split('/')
      keys = [*one_hot_dict.keys()][0]
      size = len(one_hot_dict[keys])
      bin_pattern = None

      if len(pat) > 1:
            bin_pattern = np.concatenate([one_hot_dict[pat[0]] , one_hot_dict[pat[1]]] , axis = 0)
            return bin_pattern

      else:
            tmp_arr = np.zeros(size * 2 , dtype = np.int)
            tmp_arr[size : ] = one_hot_dict[pat[0]]      
            bin_pattern = tmp_arr


      return bin_pattern



def combine_wt_matrices(pat_hop_net , dim):

      '''

      This function combines all the induvidual trained matrices into
      a single whole matrix

      '''

      weights = []

      total_weight = np.zeros((dim , dim) , dtype = np.int)

      for key , value in pat_hop_net.items():

            #weights.append(value)
            total_weight = np.add(total_weight , value)



      #weight_matrix_sum = np.sum(weights , axis = 0)

      np.fill_diagonal(total_weight , 0)
            

      return total_weight



if __name__ == '__main__':

      # Add arguments to receive Key Value pairs from Mapper

      parser = ap.ArgumentParser()
      parser.add_argument('-k' , '--key' , required = True , type = tuple)
      parser.add_argument('-v' , '--value' , required = True , type = np.matrix)

      args = parser.parse_args()

      key = args.key
      value = args.value

      pat_hop_net = {}

      pat_hop_net[key] = value

      calc_similar_patterns(pat_hop_net , rm.folder_bin_dict)

      print()

      print('Patterns trained in Day ' , rm.day)
      with open(rm.file_nm , 'a') as f:
                  f.write('Patterns trained in Day ' + rm.day)
                  f.write('\n')


      with open('Summary.txt' , 'a') as s:
            s.write('Patterns trained in Day ' + rm.day + '\n')
            s.write('\n')
            
      
      dim = rm.hop_wt_mat.shape[0]
      weight_matrix_sum = combine_wt_matrices(pat_hop_net , dim)
      rm.hop_net.set_weight(weight_matrix_sum)

      for key , value in pat_hop_net.items():

            pat = rm.folder_bin_dict[key]

            #print(pat)
            with open(rm.file_nm , 'a') as f:
                  f.write(pat + '\n')

            
      with open(rm.file_nm , 'a') as f:
            f.write('\n')

      print()

      test_idx = 0

      for tp in test_patterns:

            test_bin_pat = generate_test_bin_pattern(tp , one_hot_dict)

            with open(rm.file_nm , 'a') as f:
                  f.write('test Pattern is : ' + tp + '\n')

            # Summary output
            with open('Summary.txt' , 'a') as s:
                  s.write('Test Pattern is : ' + tp + '\n')
                  s.write('\n')            
                        

            print('Test pattern is : ' , tp)
            #while test_idx < 3:
            d_freq_accessed_path = {}

            for key , value in pat_hop_net.items():                      

                  result = hop_net.predict(test_bin_pat , n_times = 100)
                 
                  cos_sim_test = float('{: 0.2f}'.format(calcCosineSimilarity(np.array(key) , test_bin_pat)))

                  result = result[0]         

                  cos_sim_mem = '{: 0.2f}'.format(calcCosineSimilarity(np.array(key) , result))


                  with open(file_nm , 'a') as f:

                        f.write('Similarity between Memory pattern: ' + folder_bin_dict[key] +
                                      ' and result pattern: ' + folder_bin_dict[tuple(result)] + ' ' +
                                      str(cos_sim_mem) + '\n')
                        
                        #print('Similarity between Memory pattern:' ,folder_bin_dict[key] ,
                              #' and result pattern:' , folder_bin_dict[tuple(result)] , cos_sim_mem)

                  # Add those paths which are similar by approx 50%
                  if float(cos_sim_mem) > 0.45 and cos_sim_test > 0.45:

                        mem_pat = folder_bin_dict[key]

                        if mem_pat not in d_freq_accessed_path:
                              d_freq_accessed_path[mem_pat] = float(cos_sim_mem)

                        else:
                              d_freq_accessed_path[mem_pat] = float(cos_sim_mem)

                        #test_idx += 1
                              

            test_pat = tp

            # Check if any common paths are found
            if not d_freq_accessed_path:
                  print('No frequently accessed path for folder ' , test_pat , ' in day ' , day)
                  print()
                  with open('Summary.txt' , 'a') as s:
                        s.write('No frequently accessed path for folder ' + test_pat + ' in day ' + day + '\n')
                        s.write('\n')                         

            else:
                  d_freq_accessed_path = sorted(d_freq_accessed_path.items() , key = lambda x : x[1] , reverse = True)

                  print('Frequently accessed path for folder ' , test_pat , ' in day ' , day , ' is ' , )
                  for k , v in d_freq_accessed_path:
                        print(k , v)

                  print()

                        
                  with open(file_nm , 'a') as f:
                        f.write('\n')


                  with open(file_nm , 'a') as f:
                        f.write('Most frequently accessed path for folder ' + test_pat + ' in day ' + day + ' is ' + '\n')
                        

                  with open('Summary.txt' , 'a') as s:
                        s.write('Most frequently accessed path for folder ' + test_pat + ' in day ' + day + ' is ' + '\n')
                  
                        

                  with open(file_nm , 'a') as f:
                        for k , v in d_freq_accessed_path:
                              f.write(k + ' ' + str(v) + '\n')

                        f.write('\n')

                  with open('Summary.txt' , 'a') as s:
                        for k , v in d_freq_accessed_path:
                              s.write(k + ' ' + str(v) + '\n')

                        s.write('\n')


            print('Most dominant parent folder accessed in day ' , day , ' : ' , folder_bin_dict[tuple(result)])

            with open('Summary.txt' , 'a') as s:
                  s.write('Most dominant parent folder accessed in day ' + day + ' is: ' + folder_bin_dict[tuple(result)] )
