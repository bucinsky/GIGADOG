# Phd of Adriana Dunarova

import os
import sys
import shutil
import gzip
import time
import pandas as pd

from rdkit_mol2_gz import *

def unzip_mol2gz_2_mol2(mol2_gz,mol2_gz_file):
    
    src=mol2_gz_file
    mol2_file=mol2_gz+".mol2"
    print(src,mol2_file)

    with gzip.open(src, 'rb') as file_in:
        with open(mol2_file, 'wb') as file_out:
            shutil.copyfileobj(file_in, file_out)
        file_out.close()
    file_in.close()    

    return 0

def unzip_mol2gz_2_mol2_2(mol2_gz,mol2_gz_file):
    
    src=mol2_gz_file
    mol2_file=mol2_gz+".mol2"
    print(src,mol2_file)
    
    #option A
    try:
      with gzip.open(src, 'rb') as file_in:
        with open(mol2_file, 'wb') as file_out:
            shutil.copyfileobj(file_in, file_out)
        file_out.close()
      file_in.close()    
    except(OSError, ValueError):
      pass

    #option B
    # cp gz file here
    # unzip gz file

    return 0

def process_mol2_gzs(uniq_mol2_gz_tags,uniq_zincs,uniq_order_zincs):
    mol2_gz_path="/mnt/ehome-space/covid/data_sets/zinc_23aug2023/"

    for img,mol2_gz in enumerate(uniq_mol2_gz_tags):
        mol2_gz_file=mol2_gz_path+mol2_gz+".mol2.gz"
        print(img+1,mol2_gz,mol2_gz_file)

        unzip_mol2gz_2_mol2_2(mol2_gz,mol2_gz_file)

        # we have the mol2 file in our working directory now
        mol2_file=mol2_gz+".mol2"
        mol2_zincs=uniq_zincs[img]
        mol2_orders=uniq_order_zincs[img]

        #
        print(mol2_file,len(uniq_zincs[img]),len(uniq_order_zincs[img]))
        print(mol2_orders)
        print(mol2_zincs)

        # extract the mol2_orders files use the appropriate mol2_zincs name
        # and do not forget to assign the mol2_gz file tag
        get_best_pds_mo2_files(mol2_file,mol2_zincs,mol2_orders)
        
        # clean (rm) the mol2_file
        os.remove(mol2_file)

        print()

    return 0

# so we will extract and get all the mol2 files
def get_best_pds_mo2_files(mol2_file,mol2_zincs,mol2_orders):
    mol2_tag=mol2_file[:-5]

    mol2_orders_int=[]
    for mo in mol2_orders:
        mol2_orders_int.append(int(mo))

    with open(mol2_file,'r') as fi:
        for im,mol2 in enumerate(RetrieveMol2Block(fi)):
            if im in mol2_orders_int:
                indx=mol2_orders_int.index(im)
                lines=[]
                line2 = mol2.split("\n")[1].strip()

                zinc=mol2_zincs[indx]
                ozinc=mol2_orders[indx]
                print(im,ozinc,line2,zinc)
                fname=mol2_tag+"_"+zinc+"_"+str(ozinc)+".mol2"
                write_output_file_str(fname,mol2)

    return 0

def write_output_file_str(fname,string):
   f = open(fname, "w")
   f.write(string)
   f.close()
   return 0

# several zincs are from the same mol2_gz,
# we want just the  uniq mol2_gz files and which zincs are there
# as well as what is their order
def get_uniq_data(mol2_gz_tags,zincs,orders):

    uniq_mol2_gz_tags=[]
    uniq_zincs=[]
    uniq_order_zincs=[]
    # lets get unique mol2_gz_files
    for mol2_gz in mol2_gz_tags:
        if mol2_gz in uniq_mol2_gz_tags:
           continue 
        else:
           uniq_mol2_gz_tags.append(mol2_gz)
           uniq_zincs.append([])
           uniq_order_zincs.append([])
    

    for iz,zinc in enumerate(zincs):
        #print(iz,zinc)
        mol2_gz=mol2_gz_tags[iz]
        i_mol2_gz=uniq_mol2_gz_tags.index(mol2_gz)
        uniq_zincs[i_mol2_gz].append(zinc)
        order=orders[iz]
        uniq_order_zincs[i_mol2_gz].append(order)
    
    return uniq_mol2_gz_tags,uniq_zincs,uniq_order_zincs

# check whether number of zincs in the uniq_zincs is the same as for original zincs
def check_zincs_uniq_zincs_count(zincs,uniq_zincs):
    print()
    print("CHECK #zincs in uniq_zincs")
    print("Original number of zincs:",len(zincs))
    uz=0
    for u in uniq_zincs:
        uz+=len(u)
    
    print("zincs in uniq_zincs:",uz)

    return 0

# MAIN
if __name__ == "__main__":
    
    # we start the time counter
    start=time.time()
    
    # 1a; input dat file 
    best_DS_file=sys.argv[1]
    L=sys.argv[2]

    print("Preparing mol2 files for file:",best_DS_file)
    print("For letter L:",L)
    print()
    

    # 1b; read data
    df0 = pd.read_csv(best_DS_file,sep=";",comment="#")
    #print (len(df0))
    
    # get only lines with letter L 
    df=df0[df0['name'].str[0] == L]
    #print (len(df))
    
    # split the name column into three
    mol2_gz_tags = df['name'].str.split('_').str[0]
    zincs = df['name'].str.split('_').str[1]
    order_zincs = df['name'].str.split('_').str[2]
    #df['mol2_gz_tags' 'zincs', 'order_zincs']] = df['name'].str.split('_',n=-1,expand=True)
    
    mol2_gz_tags=list(mol2_gz_tags)
    zincs=list(zincs)
    order_zincs=list(order_zincs)

    #data = df.values.transpose()
    #print(len(mol2_gz_tags))
    #print(len(zincs))
    #print(len(order_zincs))
    #print(mol2_gz_tags)
    #print(zincs)
    #print(order_zincs)

    # this is the data we are interested in
    #mol2_gz_tags=data[0]
    #zincs=data[1]
    #order_zincs=data[2]

    print("Number of mol2_gz and/or ZINCS in input:",len(zincs))
    
    # 2; uniq data to have a list of zincs in uniq_zincs for each mol2_gz in uniq_mol2_gz
    uniq_mol2_gz_tags,uniq_zincs,uniq_order_zincs=get_uniq_data(mol2_gz_tags,zincs,order_zincs)
    print("Number of uniq mol2_gz:",len(uniq_mol2_gz_tags))
    #print(len(uniq_zincs))

    # 3;
    xxx=process_mol2_gzs(uniq_mol2_gz_tags,uniq_zincs,uniq_order_zincs)
    
    #end time
    end=time.time()

    print("Elapsed time is:",round(end-start,3),"seconds\n")
