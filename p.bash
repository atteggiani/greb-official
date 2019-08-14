#!/bin/bash
# vals=($(seq 0.974 0.0002 0.98))
for a in 0.9798 0.98
do
    ./myjobscript.bash -e 931 -y 80 -a -s ~/university/phd/greb-official/artificial_solar_radiation/sw.artificial.frominput_x${a}.ctl
done
exit
