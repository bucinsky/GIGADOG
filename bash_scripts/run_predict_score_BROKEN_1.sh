#!/bin/bash

# Python 3.9 is needed for xyz correction script
#export PATH=/ehome/PROGS/python/Python-3.9.0_build/bin:$PATH
source ~/.venv_python3.11/bin/activate

# load OpenBabel
module load OpenBabel/3.1.1-gompi-2025b

# current directory
here=`pwd`

# log file
out=$here/BROKEN_make_xyz.txt


date > $out
echo "START creating xyz files from broken mol2.gz files" >> $out
echo >> $out

i=1

# find all broken mol2.gz files in current directory
L_mol2_gz_files=`ls *.mol2.gz`

for f in $L_mol2_gz_files
do
    echo "$i processing $f" >> $out
    # decompress mol2.gz -> mol2
    #gzip -d $f
    gzip -df $f
    # remove .gz extension
    f2=${f::-3}
    # remove .mol2 extension to get xyz name
    fxyz=${f2::-5}
    echo "Creating ${fxyz}.xyz" >> $out

    # convert mol2 to xyz format using OpenBabel
    obabel $f2 -o xyz > ${fxyz}.xyz0

    # correct xyz format
    python3 $GDR/python_codes/correct_xyz_from_obabel.py ${fxyz}.xyz0 >> $out

    # remove temporary xyz file
    rm ${fxyz}.xyz0

    i=$((i+1))

done

echo >> $out
echo "XYZ files done." >> $out
date >> $out
echo "ENDE" >> $out



