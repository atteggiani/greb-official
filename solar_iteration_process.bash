#!/bin/bash
# Author: Davide Marchegiani
PROGNAME=$0

usage() {
  cat << EOF
Usage: $PROGNAME [-i <tot_iter>] [-n <tsurf>] ...

Possible keys:
-o -> change solar radiation only over oceans
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
    (h) usage
        exit 0;;
    (*) usage
  esac
done

((${tot_iter:=20}))

wdir=$(pwd)
# Files for 1st iteration
tsurf=${tsurf:="${wdir}/output/scenario.exp-931.geoeng.2xCO2.sw.artificial.frominput_x0.98_50yrs"}
tsurf_init=$tsurf
sim_years=${tsurf##*_};sim_years=${sim_years%.*}

# Initialize iterations
niter=1
while (( $niter <= $tot_iter )); do
    # Create solar matrix
    echo -e "\nIter. ${niter}/${tot_iter} -- Creating new solar matrix..."
    python solar_iteration.py $niter $tsurf $ocean_flag
    pad="Iter. ${niter}/${tot_iter} "
    # RUN GREB

    printf "%*s%b" ${#pad} '' "-- Run GREB\n"
    ./myjobscript.bash -y ${sim_years%yrs} -s "${wdir}/artificial_solar_radiation/sw.artificial.iteration${ocean_flag}/sw.artificial.iter${niter}${ocean_flag}" -e 931
    # Change files for next iteration
    tsurf="${wdir}/output/scenario.exp-931.geoeng.2xCO2.sw.artificial.iter${niter}${ocean_flag}_${sim_years}"
    ((niter++))
done
echo -e "\nPlotting iterations...\n"
python ./plot_iter.py -i $tsurf_init -f 'solar' -o $ocean_flag
echo -e "DONE!!\n"
exit
