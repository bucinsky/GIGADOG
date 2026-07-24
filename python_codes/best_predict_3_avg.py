
# import glob and pandas as pd
import glob

# defining function which open and read file
def read_file(file_name):
    with open(file_name, "r") as f:
        lines = f.readlines()
    return lines  # the value to be returned

# our csv file looks like this:
#    0; 1; 2; 3; 4; 5
# name;01;02;03;04;05
# ZINC000167595693;-6.8399677;-6.422313;-6.3123174;-6.9600945;-6.372164
def get_best_pds(lines,ds_lim):
    best_pds_lines=[]    
    # we loop from 1 since in line 0 is the head for pandas
    for iline,line in enumerate(lines[1:]):
        sline=line.split(";")
        # we check whether a predicted docking score (pds) is below ds_lim
        avg=float(sline[1])+float(sline[2])+float(sline[3])+float(sline[4])+float(sline[5])
        avg=avg/5
        if avg < ds_lim:
           #TODO: we can add average and stdev as well
           best_pds_lines.append(line.rstrip()+";"+str(iline))
    
    return best_pds_lines

# defining function which open, write and then  close file_out_best_pds 
def write_output_file_from_list(file_out_best_pds,best_pds_compounds):
   f = open(file_out_best_pds, "w")
   for l in best_pds_compounds:
       f.write(l+'\n')
   f.close()

# we get all the csv files in a given dir
files = glob.glob("*.csv")

# file with best ds below ds_lim 
ds_lim=-9.0

# list with best ds compounds and the ZINC15 file tag according to the
best_pds_compounds=[]
# zinc15_file;name;01;02;03;04;05;#order in zinc15_file
best_pds_compounds.append("zinc15_file;name;01;02;03;04;05;#order")

# we loop through our csv files
for file_name in files:
    # here is the content=lines of file_name
    lines=read_file(file_name)
    # let us find the best dockers / best DS
    best_pds_lines=get_best_pds(lines,ds_lim)
    # we need the name for the sdf/mol2 file from ZINC15 which is hidden in the
    # file_name:
    zinc15_name0=file_name.split("/")[-1]
    zinc15_name=zinc15_name0.split("_")[0]
    # we add zinc15_name to best_pds_lines and add this to best_pds_compounds
    for bpdsl in best_pds_lines:
        best_pds_compounds.append(zinc15_name+";"+bpdsl)

# we write out best_pds_compounds into a file
ids_lim=int(abs(ds_lim))
file_out_best_pds="best_pds_3_avg_"+str(ids_lim)+".dat"
write_output_file_from_list(file_out_best_pds, best_pds_compounds)


