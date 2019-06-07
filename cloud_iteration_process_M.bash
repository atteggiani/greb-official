#!/bin/bash
# Total number of iterations
tot_iter=$1
((${tot_iter:=5}))

wdir="/Users/dmar0022/university/phd/greb-official"
# Files for 1st iteration
cld_old="${wdir}/input/isccp.cloud_cover.clim.bin"
cld_new="${wdir}/artificial_clouds/cld.artificial.frominput_x1.1"
sc_old="${wdir}/output/scenario.exp-20.2xCO2"
sc_new="${wdir}/output/scenario.exp-930.geoeng.cld.artificial.frominput_x1.1"
# Initialize iterations
niter=1
while (( $niter <= $tot_iter )); do
    echo -e "\nCreating new cloud matrix -- Iter. ${niter}/${tot_iter}"
    python cloud_iteration.py $cld_old $cld_new $sc_old $sc_new $niter
    echo -e "Run GREB -- Iter. ${niter}/${tot_iter}\n"
    ${wdir}/myjobscript.bash "${wdir}/artificial_clouds/cld.artificial.iter${niter}"
# Change files for next iteration
cld_old=$cld_new
sc_old=$sc_new
cld_new="${wdir}/artificial_clouds/cld.artificial.iter${niter}"
sc_new="${wdir}/output/scenario.exp-930.geoeng.${cld_new##*/}"
((niter++))
done
exit
