#!/bin/bash

# current working directory
here=`pwd`

# output file with histogram values for all letters
outfile="get_all_pds_avg_to_one_dat_file.dat"

# the header
echo "L;-15.0;-14.0;-13.0;-12.0;-11.0;-10.0;-9.0;-8.0;-7.0;-6.0;-5.0;-4.0;-3.0;-2.0;" > "$outfile"

# process all letters
for L in A B C D E F G H I J K
do
    
    cd "xyz_${L}_predict" || continue 

    echo
    echo "Processing ${L}..."

    # run the py script and keep only the histogram line
    line=$(python3 $GDR/python_codes/all_predict_3_avg.py | grep "^counts;")

    # remove the "counts;" prefix and write the results to the output file
    echo "${L};${line#counts;}" >> "$here/$outfile"

    cd "$here"

done

echo
echo "Histogram data were written to:"
echo "$outfile"
echo
echo "Done."


