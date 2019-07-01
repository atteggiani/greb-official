#!/bin/bash
# Total number of iterations

tot_iter="$1"
t="$2"
flag="$3" #default is "FIXED", can be set to "NOT_FIXED"
t_new="$4"
t_old_r="$5"


((${tot_iter:=5}))
t=${t:='monthly'}
flag=${flag:='FIXED'}
if [ "$flag" == "NOT_FIXED" ] || [ "$flag" == "nf" ] || [ "$flag" == "not_fixed" ]
then
    t="${t}_nf"
fi
wdir="/Users/dmar0022/university/phd/greb-official"
# Files for 1st iteration
t_new=${t_new:="${wdir}/output/scenario.exp-930.geoeng.cld.artificial.frominput_x1.1"}
t_new_r="$t_new"
t_old_r=${t_old_r:="${wdir}/output/scenario.exp-20.2xCO2"}
t_iter="$t_new"
# Initialize iterations
niter=1
while (( $niter < $niter+$tot_iter )); do
    echo -e "\nIter. ${niter}/${tot_iter} -- Creating new cloud matrix..."
    python cloud_iteration.py $niter $t $t_new $t_new_r $t_old_r
    pad="Iter. ${niter}/${tot_iter} "
    printf "%*s%b" ${#pad} '' "-- Run GREB\n"
    ${wdir}/myjobscript.bash "${wdir}/artificial_clouds/cld.artificial.iter${niter}_${t}"
    # Change files for next iteration
    t_new="${wdir}/output/scenario.exp-930.geoeng.cld.artificial.iter${niter}_${t}"
    if [ "$flag" == "NOT_FIXED" ] || [ "$flag" == "nf" ] || [ "$flag" == "not_fixed" ]
    then
        t_old_r="$t_new_r"
        t_new_r="$t_new"
    fi
    ((niter++))
done
echo -e "\nPlotting iterations...\n"
python ${wdir}/plot_iter.py $t $t_iter
echo -e "DONE!!\n"
exit
