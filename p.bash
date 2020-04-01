#!/bin/bash

coeff=$(seq 0.950 0.002 0.976)
for a in $coeff;
do
    echo "Coeff = ${a}"
    /Users/dmar0022/university/phd/greb-official/myjobscript.bash -e 933 -y 50 -s /Users/dmar0022/university/phd/greb-official/artificial_solar_radiation/sw.artificial.frominput_x${a} -a
done
