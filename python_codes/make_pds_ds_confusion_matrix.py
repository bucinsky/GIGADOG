
import matplotlib.pyplot as plt
import matplotlib as mlb
#from matplotlib.ticker import MultipleLocator
#from sklearn.metrics import mean_squared_error
import pandas as pd
import numpy as np
from scipy import stats
import time
import sys
import os.path
import glob

# defining function which open and read file
def read_file(file_name):
    with open(file_name, "r") as f:
        lines = f.readlines()
    return lines  # the value to be returned

#
def convert_to_float(sx):
    x=[]
    for s in sx:
        x.append(float(s))
    return x    

# get the histogram
def get_histogram(lines,TDS):
    #T=[0,0,0,0,0,0,0,0,0,0] # total counts
    #FN=[0,0,0,0,0,0,0,0,0,0] # FN counts
    T=  [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    FN= [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] 
    FN2=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] 
    FN3=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] 
    for line in lines:
        sline=line.split(";")
        # VERY IMPORTANT TO SET THE INTEGERS ACCORDINGLY
        avg=float(sline[1])
        avg_new=float(sline[2])
        #avg_new
        ds=float(sline[3])
    
        # where to put the avg value
        # index 
        #i=int(abs((avg+10))*10.)
        i=int(-(avg+9)*10.)
        if i < 0:
           i=-i
        if i >= 20:
           i=20
        #   print(line)
        #print(avg,i)
        T[i]+=1
        if ds <= TDS:
           FN[i]+=1
        if avg_new <= TDS:
           FN2[i]+=1
        if avg_new <= TDS and ds <= TDS:
           FN3[i]+=1
        
    return T,FN,FN2,FN3

# lazy MAIN

# 1; read input
#fin="X_comparison_pds10_scores_all.csv"
#fin="X_comparison_pds_-10.0_-9.9_scores_all.csv"
#fin="X_comparison_pds_merge.csv"
fin="X_comparison_pds10_scores_sample.csv"
#fin=sys.argv[1]
lines=read_file(fin)
print("input "+fin+" read\n")

#fin2=sys.argv[2]
#lines2=read_file(fin2)
#print("input 2 read\n")

# we will fill in the counts of the confusion matrix
# let us do the list of AVG_DS[ai][di]
AVG_DS=[
[0,0,0,0,0],
[0,0,0,0,0],
[0,0,0,0,0],
[0,0,0,0,0],
[0,0,0,0,0]]

thr=-8.
for il,line in enumerate(lines[1:]):
    sline=line.split(";")
    # VERY IMPORTANT TO SET THE INTEGERS ACCORDINGLY
    avg=float(sline[1])
    avg_new=float(sline[2])
    ds=float(sline[3])
    #xs=lines2[il+1].split(";")
    #x=float(xs[1])
    x = avg
    if x > thr:
    #or if avg > thr:
        continue

    i=int(-round((avg+9.0),6))
    if i < 0:
       i=0
    if i > 4:
       i=4
    
    j0=int(-round((ds+9.0),6))
    j=-(j0-4)
    #j=int(round(ds+14.0,6))
    if j < 0:
       j=0
    if j > 4:
       j=4
    AVG_DS[i][j]+=1

# print confusion matrix
print("Confusion matrix with thr:",thr)
for i in range(len(AVG_DS)):
    print(AVG_DS[i])

# compound cound below thr
s=0
for i in range(len(AVG_DS)):
   for j in range(len(AVG_DS)):
       s+=AVG_DS[i][j]

print()
print("Columns are: (-20;-13>,(-13;-12>,(-12;-11>,(-11;-10>,(-10;-0>")
print("Lines are  :   (-10;0>,(-11;-10>,(-12;-11>,(-13;-12>,(-20;-13>")

print()
print("All compounds:",len(lines[1:]),s)
print("Compounds below thr:",s)
print("Threshold (thr):",thr,"kcal/mol")
