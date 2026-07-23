#!/bin/bash

#SBATCH --job-name="JOBX"
#SBATCH --nodes=1
#SBATCH --ntasks=12
#SBATCH --partition=compute_mem
#SBATCH --time=12:00:00

#threads=OMPX
export OMP_NUM_THREADS=$SLURM_NPROCS

# we need to activate python3 of our choice
#export PATH=/ehome/PROGS/python/Python-3.9.0_build/bin:$PATH
#or
#module load python3.11
#or
source ~/.venv_python3.11/bin/activate
#or whatever suits you

# these values are automatically replaced by the do_run_predict_score.sh
L=LX
N=NX

fl=XFL
ll=XLL

#
L_txt=$GDR/mol2_data_files/${L}.csv

mol2_gz_dir=$GDR/mol2_gz_files

# out is in the $out file
here=`pwd`
out=$here/${L}${N}_predict.txt
date > $out

# work dir 
#work_dir=/work/$USER/xyz_${L}${N}_predict
work_dir=/work_nvme/$SLURM_JOB_ID
cd $work_dir

# here we prepare the list of mol2.gz files to be processed
L_mol2_gz_files=`cat $L_txt | sed -n "${fl},${ll}p" | cut -f1 -d";"`

echo "START ${L}${N}" >> $out
echo "Input txt: $L_txt" >> $out
echo "$fl and $ll" >> $out
echo >> $out

# lets make the xyz from the mol2.gz 
echo 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX' >> $out
echo >> $out

i=1

echo "Preparing xyz files:" >> $out
date >> $out
for fname in $L_mol2_gz_files
do
  f=$mol2_gz_dir/${fname}.mol2.gz
  echo $i prepare $f >> $out 
  
  python3  $GDR/python_codes/make_xyz_from_mol2.py $f >> $out 
  
  i=$((i+1))

done
echo "xyz files done." >> $out
date >> $out
echo >> $out

# DS prediction
echo 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX' >> $out
echo >> $out

i=1

echo "DS prediction starts:" >> $out
date >> $out

# load the necessary prediction settings for SchNetPack model at:
# https://github.com/j-matuska/schnet_hyperparameters_optimization
#
#export PATH=/ehome/PROGS/python/Python-3.8.6_build/bin:$PATH
#export ML_PATH=/ehome/PROGS/python/Python-3.8.6_build/lib

csv_result_dir=$GDR/csv_result_files

for fxyz in `ls ${L}*.xyz`
do
   echo $i DS $fxyz >> $out 
   # actual prediction needs to be adjusted with respet to the  SchNetPack model of Matuska
   #python3 /ehome/PROGS/misc/schnetpack_models/predict.py $fxyz
    
   # just a formal something to run
   wc -l $fxyz >> Schnet03_6_10Ang_train80.log
   echo >> Schnet03_6_10Ang_train80.log
   sleep 1 #(we pretend that the calculation lasts 1 second)
   fname=`echo $fxyz | sed 's/.xyz//'`
   cp $csv_result_dir/${fname}_Schnet03_6_10Ang_train80.csv .
   
   i=$((i+1))
done 
echo "DS prediction done." >> $out
date >> $out 
echo >> $out
rm *xyz

mv Schnet03_6_10Ang_train80.log ${L}${N}_Schnet03_6_10Ang_train80.log
cd $here
cp -r $work_dir/* .
date >> $out 
echo "ENDE" >> $out
