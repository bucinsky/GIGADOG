#!/bin/bash

export OMP_NUM_THREADS=6

# current directory
here=`pwd`

# output file
out=$here/BROKEN_predict.txt

date > $out
echo "START SchNet prediction for broken xyz files" >> $out
echo >> $out

echo "Input xyz files:" >> $out
ls *.xyz >> $out
echo >> $out

i=1

echo "DS prediction starts:" >> $out
date >> $out

# predict all xyz broken files in current directory
# load the necessary prediction settings for SchNetPack model at:
# https://github.com/j-matuska/schnet_hyperparameters_optimization

csv_result_dir=$GDR/csv_result_files

for fxyz in `ls *.xyz`
do
    echo "$i predicting $fxyz" >> $out

    #python3.8 /ehome/PROGS/misc/schnetpack_models/predict.py $fxyz
    
    # just a formal something to run
    wc -l $fxyz >> Schnet03_6_10Ang_train80.log
    echo >> Schnet03_6_10Ang_train80.log
    sleep 1 #(we pretend that the calculation lasts 1 second)
    fname=`echo $fxyz | sed 's/.xyz//'`
    cp $csv_result_dir/${fname}_Schnet03_6_10Ang_train80.csv .

    i=$((i+1))

done

echo >> $out
echo "DS prediction done." >> $out
date >> $out
rm *.xyz

# save SchNet log with a different name
mv Schnet03_6_10Ang_train80.log BROKEN_Schnet03_6_10Ang_train80.log

echo "ENDE" >> $out
date >> $out


