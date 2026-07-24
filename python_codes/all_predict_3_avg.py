
import math
import glob
import time

# defining function which open and read file
def read_file(file_name):
    with open(file_name, "r") as f:
        lines = f.readlines()
    return lines  # the value to be returned

# our csv file looks like this:
#    0; 1; 2; 3; 4; 5
# name;01;02;03;04;05
# ZINC000167595693;-6.8399677;-6.422313;-6.3123174;-6.9600945;-6.372164
def get_all_pds(lines):
    all_pds_lines=[]    
    # skip the header line
    for iline,line in enumerate(lines[1:]):
        sline=line.split(";")
        # calculate the average predicted docking score (avg_pds) from the five predictions
        avg=float(sline[1])+float(sline[2])+float(sline[3])+float(sline[4])+float(sline[5])
        avg=avg/5.0

        if avg < -15.0:
           print(line.strip(),avg) 
        
        all_pds_lines.append(avg)
    
    return all_pds_lines

start=time.time()

# we get all the csv files in a given dir
files = glob.glob("*.csv")

counts=[0]*14
cneg=0
cpos=0
cnan=0

# process all csv files in current directory
for file_name in files:
    # read one csv file
    lines=read_file(file_name)
    # calculate avg_pds
    all_pds_lines=get_all_pds(lines)
    
    # count structures in 1 kcal/mol pds intervals
    for b in all_pds_lines:
        if math.isnan(b):
           cnan+=1
           continue
        ib=int(b)
        iib=ib-1+15
        if ib < -14:
           if ib > -20:
              counts[0]+=1
           else:    
              cneg+=1
           continue
        if ib > -1:
           cpos+=1
           continue
        counts[iib]+=1

end=time.time()
dt=end-start
print("time=",round(dt,3),"sec")

# print histogram in one line
# this line will be parsed automatically by the bash script
print("counts;" + ";".join(str(c) for c in counts) + ";")

print("counts below -15 kcal/mol:",cneg)
print("counts above  -1 kcal/mol:",cpos)
print("counts of NaN            :",cnan)
print()

for c in counts:
    print(c)
print()
