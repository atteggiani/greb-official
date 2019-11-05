#!/bin/bash
# Author: Davide Marchegiani
PROGNAME=$0

usage() {
  cat << EOF
Usage: $PROGNAME [-i <tot_iter>] [-n <t_new>] [-f] ...

Possible keys:
-O -> change clouds only over oceans
-f -> set a FIXED sensitivity coefficient
-i -> total number of iterations
-n -> new tsurf pattern
-o -> old tsurf pattern


EOF
  exit 1
}

while getopts hOfi:n:o: opt; do
  case $opt in
    (O) ocean_flag="_ocean";;
    (f) fixed_flag="_f";;
    (i) tot_iter=$OPTARG;;
    (n) t_new=$OPTARG;;
    (o) t_old_r=$OPTARG;;
    (*) usage
  esac
done

((${tot_iter:=5}))
fixed_flag=${fixed_flag:="_nf"}

wdir=$(pwd)
# Files for 1st iteration
t_new=${t_new:="${wdir}/output/scenario.exp-930.geoeng.cld.artificial.frominput_x1.1${ocean_flag}_50yrs"}
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
    python cloud_iteration.py $niter $t_new $t_new_r $t_old_r $fixed_flag $ocean_flag
    pad="Iter. ${niter}/${tot_iter} "
    printf "%*s%b" ${#pad} '' "-- Run GREB\n"
    ${wdir}/myjobscript.bash -y ${sim_years%yrs} -c "${wdir}/artificial_clouds/cld.artificial.iteration_monthly${fixed_flag}${ocean_flag}/cld.artificial.iter${niter}_monthly${fixed_flag}${ocean_flag}"
    # Change files for next iteration
    t_new="${wdir}/output/scenario.exp-930.geoeng.cld.artificial.iter${niter}_monthly${fixed_flag}${ocean_flag}_${sim_years}"
    if [ "$fixed_flag" == "_nf" ]
    then
        t_old_r="$t_new_r"
        t_new_r="$t_new"
    fi
    ((niter++))
done
echo -e "\nPlotting iterations...\n"
if [[ "$ocean_flag" == "" ]];then
    ocean_flag="-"
fi
python ${wdir}/plot_iter.py $fixed_flag $ocean_flag $t_iter ${sim_years%yrs}
echo -e "DONE!!\n"
exit
