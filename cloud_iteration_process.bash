#!/bin/bash
# Author: Davide Marchegiani
PROGNAME=$0

usage() {
  cat << EOF
Usage: $PROGNAME [-i <tot_iter>] [-n <tsurf>] ...

Possible keys:
-o -> change clouds only over oceans
-i -> total number of iterations
-n -> new tsurf pattern

EOF
  exit 1
}

while getopts hi:n:o: opt; do
  case $opt in
    (o) ocean_flag="_ocean";;
    (i) tot_iter=$OPTARG;;
    (n) tsurf=$OPTARG;;
    (*) usage
  esac
done

((${tot_iter:=5}))

wdir=$(pwd)
# Files for 1st iteration
tsurf=${tsurf:="${wdir}/output/scenario.exp-930.geoeng.cld.artificial.frominput_x1.1_50yrs"}
tsurf_init=$tsurf
sim_years=${tsurf##*_};sim_years=${sim_years%.*}

# Initialize iterations
niter=1
while (( $niter <= $tot_iter )); do
    # Create cloud matrix
    echo -e "\nIter. ${niter}/${tot_iter} -- Creating new cloud matrix..."
    python cloud_iteration.py $niter $tsurf $ocean_flag
    pad="Iter. ${niter}/${tot_iter} "
    # RUN GREB

    printf "%*s%b" ${#pad} '' "-- Run GREB\n"
    ./myjobscript.bash -y ${sim_years%yrs} -c "${wdir}/artificial_clouds/cld.artificial.iteration${ocean_flag}/cld.artificial.iter${niter}${ocean_flag}"
    # Change files for next iteration
    tsurf="${wdir}/output/scenario.exp-930.geoeng.cld.artificial.iter${niter}${ocean_flag}_${sim_years}"
    ((niter++))
done
echo -e "\nPlotting iterations...\n"
python ./plot_iter.py $tsurf_init $ocean_flag
echo -e "DONE!!\n"
exit
