#!/bin/bash
# Total number of iterations

tot_iter="$1"
flag="$2" #default is "NOT_FIXED" (or "nf"), can be set to "FIXED" (or "f")
t_new="$3"
t_old_r="$4"

((${tot_iter:=5}))
flag=${flag:="nf"}
if [ "$flag" == "nf" ] || [ "$flag" == "not_fixed" ]
then
    flag="_nf"
else
    flag=""
fi
wdir="/Users/dmar0022/university/phd/greb-official"
# Files for 1st iteration
t_new=${t_new:="${wdir}/output/scenario.exp-930.geoeng.cld.artificial.frominput_x1.1_50yrs"}
t_new_r="$t_new"
t_old_r=${t_old_r:="${wdir}/output/scenario.exp-20.2xCO2_50yrs"}
t_iter="$t_new"
sim_years=${t_new##*_};sim_years=${sim_years%.*}

# Initialize iterations
if [[ $t_new_r == *"iter"* ]]; then
    niter=${t_new_r##*iter};niter=$((${niter%%_*}+1))
else
    niter=1
fi
tot_iter=$(($tot_iter + $niter - 1))

while (( $niter <= $tot_iter )); do
    echo -e "\nIter. ${niter}/${tot_iter} -- Creating new cloud matrix..."
    python cloud_iteration.py $niter $t_new $t_new_r $t_old_r $flag
    pad="Iter. ${niter}/${tot_iter} "
    printf "%*s%b" ${#pad} '' "-- Run GREB\n"
    ${wdir}/myjobscript.bash -y ${sim_years%yrs} -c "${wdir}/artificial_clouds/cld.artificial.iteration_monthly${flag}/cld.artificial.iter${niter}_monthly${flag}"
    # Change files for next iteration
    t_new="${wdir}/output/scenario.exp-930.geoeng.cld.artificial.iter${niter}_monthly${flag}_${sim_years}"
    if [ "$flag" == "_nf" ]
    then
        t_old_r="$t_new_r"
        t_new_r="$t_new"
    fi
    ((niter++))
done
echo -e "\nPlotting iterations...\n"
python ${wdir}/plot_iter.py $flag $t_iter ${sim_years%yrs}
echo -e "DONE!!\n"
exit
