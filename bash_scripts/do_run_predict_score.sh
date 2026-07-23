#!/bin/bash

# detect letter from current directory name
# which MUST be in the form xyz_L_predict with L one of letters: ABCDEFGHIJK
current_dir=$(basename "$PWD")
L=$(echo "$current_dir" | sed 's/xyz_//' | sed 's/_predict//')

echo "For letter: $L"

# maximum number of structures per PBS job
max_structures=10000

# file with mol2.gz name tag and number of compounds
L_txt=$GDR/mol2_data_files/${L}.csv

# pbs prototype where we wnat to change L (denoted as LLL) and N (denoted as NNN)
pbs_proto_file=$GDR/bash_scripts/run_predict_score_prototype.sh

# check if csv file exists
if [ ! -f "$L_txt" ]; then
    echo "ERROR: File not found:"
    echo "$L_txt"
    exit 1
fi

# count structures
#nstructures=$(wc -l < "$L_txt")
# -F";" uses ';' as the column separator
# $2 is the second column (number of structures)
# sum all values in the second column
nstructures=$(awk -F";" '{sum += $2} END {print sum}' "$L_txt")
echo "Number of structures: $nstructures"

# job limits
job_limits_file=job_limits_${L}.out
rm -f $job_limits_file

job=1
start=1
sum=0
line=0


while IFS=";" read -r name count
do
    line=$((line+1))
    sum=$((sum+count))

    if [ $sum -ge $max_structures ]; then
        echo "${job};${start};${line};${sum}" >> $job_limits_file
        job=$((job+1))
        start=$((line+1))
        sum=0
    fi

done < "$L_txt"

# add remaining structures
if [ $start -le $line ]; then
    echo "${job};${start};${line};${sum}" >> $job_limits_file
fi

# number of jobs
NJOBS=$(wc -l < $job_limits_file)
echo "Number of jobs to create: $NJOBS"

N=1

while IFS=";" read -r job fl ll structures
do

    pbs_file=run_predict_score_${L}${N}.sh
    job_name=rp_${L}${N}

    echo ""
    echo "$pbs_file"
    echo "CSV lines: $fl - $ll"
    echo "Structures: $structures"

    # copy prototype
    cp $pbs_proto_file $pbs_file
    # replace job name
    sed -i "s/JOBX/${job_name}/g" $pbs_file
    # replace letter
    sed -i "s/LX/${L}/g" $pbs_file
    # replace job number
    sed -i "s/NX/${N}/g" $pbs_file
    # replace first line
    sed -i "s/XFL/${fl}/g" $pbs_file
    # replace last line
    sed -i "s/XLL/${ll}/g" $pbs_file

    # when we want to run automatically
    sbatch $pbs_file
    sleep 1

    N=$((N+1))

done < $job_limits_file

echo ""
echo "sh files created and launched."



