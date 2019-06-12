#!/bin/bash
# Total number of iterations

tot_iter="$1"
t="$2"
cld_old="$3"
cld_new="$4"

t=${t:='monthly'}
wdir="/Users/dmar0022/university/phd/greb-official"
# Files for 1st iteration
((${tot_iter:=5}))
cld_old=${cld_old:="${wdir}/input/isccp.cloud_cover.clim.bin"}
cld_new=${cld_new:="${wdir}/artificial_clouds/cld.artificial.frominput_x1.1"}
if [ "${cld_old}" == "${wdir}/input/isccp.cloud_cover.clim.bin" ]; then
    sc_old="${wdir}/output/scenario.exp-20.2xCO2"
else
    sc_old="${wdir}/output/scenario.exp-930.geoeng.${cld_old##*/}"
fi
sc_new="${wdir}/output/scenario.exp-930.geoeng.${cld_new##*/}"
# Initialize iterations
if [ "$cld_new" == *".iter"* ]; then
    niter=${cld_new##*.iter}
    niter=${niter%%.*}
    niter=${niter%%_*}
else
    niter=1
fi

while (( $niter <= $tot_iter )); do
    echo -e "\nIter. ${niter}/${tot_iter} -- Creating new cloud matrix..."
    python p.py $cld_old $cld_new $sc_old $sc_new $niter $t
    # python cloud_iteration.py $cld_old $cld_new $sc_old $sc_new $niter $t
    pad="Iter. ${niter}/${tot_iter} "
    printf "%*s%b" ${#pad} '' "-- Run GREB\n"
    ${wdir}/myjobscript.bash "${wdir}/artificial_clouds/cld.artificial.iter${niter}_${t}"
# Change files for next iteration
cld_old=$cld_new
sc_old=$sc_new
cld_new="${wdir}/artificial_clouds/cld.artificial.iter${niter}_${t}"
sc_new="${wdir}/output/scenario.exp-930.geoeng.${cld_new##*/}"
((niter++))
done
echo -e "\nPlotting iterations...\n"
python ${wdir}/plot_iter.py $t
echo -e "DONE!!\n"
exit
