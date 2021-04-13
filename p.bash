#!/bin/bash
base_dir=/Users/dmar0022/university/phd/greb-official
output_dir=$base_dir/output
n_year_run=30

# Run GREB experiments in parallel
num_parallel_run=5
n_threads=2
files=(sw1 sw2 sw3 sw4 sw5)
tot=${#files[@]}
rest=$(( tot - (tot/num_parallel_run)*num_parallel_run ))

i=0
while [[ $i -lt $tot ]]
do
    echo "RUN GREB - $((i+num_parallel_run))/$tot ===================================================================================="
    sw=(${files[@]:$i:$num_parallel_run})
    run_command=""
    for n in $(seq 1 $num_parallel_run); do 
        echo "$n - $(basename ${sw[((n-1))]})"
        run_command+="/Users/dmar0022/university/phd/greb-official/myjobscript.bash -e 931 -y $n_year_run -s ${sw[$((n-1))]} -w $base_dir/work${n} -t $n_threads & "
    done
    # !!!!!!!!!!!!!!!! THE NUMBER OF THE LINES BETWEEN THE EXCLAMATION POINTS MUST BE EQUAL TO num_parallel_run !!!!!!!!!!!!!!!!
    # /Users/dmar0022/university/phd/greb-official/myjobscript.bash -e 931 -y $n_year_run -s ${sw[0]} -w $base_dir/work1 -t $n_threads & \
    # /Users/dmar0022/university/phd/greb-official/myjobscript.bash -e 931 -y $n_year_run -s ${sw[1]} -w $base_dir/work2 -t $n_threads & \
    # /Users/dmar0022/university/phd/greb-official/myjobscript.bash -e 931 -y $n_year_run -s ${sw[2]} -w $base_dir/work3 -t $n_threads & \
    # /Users/dmar0022/university/phd/greb-official/myjobscript.bash -e 931 -y $n_year_run -s ${sw[3]} -w $base_dir/work4 -t $n_threads & \
    # /Users/dmar0022/university/phd/greb-official/myjobscript.bash -e 931 -y $n_year_run -s ${sw[4]} -w $base_dir/work5 -t $n_threads 
    # # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    echo ${run_command%& }
    # wait
    i=$((i+num_parallel_run))
done