#!/bin/bash
# vals=($(seq 0.978 0.0002 0.985))
# for a in ${vals[@]}
# do
#     ./myjobscript.bash -e 931 -y 80 -a -s ~/university/phd/greb-official/artificial_solar_radiation/sw.artificial.frominput_x${a}.ctl
# done
# exit

t_new="output/scenario.exp-930.geoeng.cld.artificial.frominput_x1.1_50yrs"
a=${t_new##*_*yrs}
# echo "${a%yrs}"
echo "$a"
