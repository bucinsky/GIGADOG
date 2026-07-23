
# import modules
import glob
import time
import sys
import os

import numpy as np

# we use a specific functiosn from a py file in this dir
from rdkit_mol2_gz import *

# mol2 manipulation to xyz 
def use_mol2s_for_letter(letter):
   
   # we start the time counter
   start=time.time()
   
   # path to the dir wheer the sdf.gz files are present
   gdr = os.environ["GDR"]
   dir_mol2s = os.path.join(gdr, "mol2_gz_files")
   
   # lets read all the mol2.gz files
   gz_mol2s= glob.glob(dir_mol2s+'/*.mol2.gz')
   print("Total number of mol2.gz files:",len(gz_mol2s),"in",dir_mol2s)

   # check time needed for this
   now=time.time()
   print("Time to get here:",round(now-start,3),"seconds\n")
   print("LETTER:",letter,"\n")
   
   # we will inquire only files beginning with the letter in input variable 
   # letter
   A_gz_mol2s=[]
   for gz_mol2 in gz_mol2s:
       mol2_name=gz_mol2.split("/")[-1]
       if mol2_name[0]==letter:
          #print(gz_mol2)
          A_gz_mol2s.append(gz_mol2)
   
   # we clear the gz_mol2s list with all letter file names
   gz_mol2s.clear()
   
   print("Number of",letter,"mol2.gz files:",len(A_gz_mol2s))
   now=time.time()
   print("Time to get here:",round(now-start,3),"seconds\n")
   
   A_counts=[]
   
   # here we count the number of compounds in each mol2.gz file
   for ia,A_gz_mol2 in enumerate(A_gz_mol2s):
       print(ia,A_gz_mol2)
       A_count=0
       #A_count=process_mol2gz_to_xyz(A_gz_mol2)
       A_count=rdkit_process_mol2_gz_file(A_gz_mol2)
       print(A_count)
       print()
       A_counts.append(A_count)
       if ia >= 9: break
   
   # here we get the total sum
   print("Total number of compounds is:",np.sum(A_counts))
   
   #end time
   end=time.time()
   print("Elappsed time is:",round(end-start,3),"seconds\n")

# MAIN
if __name__ == "__main__":
    
    file_mol2_gz=sys.argv[1]

    mol2_count=rdkit_process_mol2_gz_file_to_xyz(file_mol2_gz) 

