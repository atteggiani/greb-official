#!/bin/bash
# run script for geoscenario experiments with the Globally Resolved Energy Balance (GREB) Model
# Author: Davide Marchegiani

# create work directory if does not already exist
if [ ! -d work ]
then
    mkdir work
else
# else clean up work directory
    rm -f work/*
fi

#####################
# BEGIN USER INPUT! #
#####################

# settings the experiment number for scenario run
EXP=930 # Geo-Engineering experiment with the artificial clouds forcing

# Setting flag for saving control output (1 = save control, 0 = don't save control)
output_control=0

# length of sensitivity experiment in years
YEARS=50

# Set the name of the binary file containing the artificial clouds input for scenario
# run (with or without .bin).
# If no file is provided, the default one '../input/cld.artificial.bin' will be used.
cld_artificial="$1"
cld_artificial=${cld_artificial:='../artificial_clouds/cld.artificial.bin'}
# ###################
# # END USER INPUT! #
# ###################
### compile GREB model (uncomment one of these three options)
gfortran -Ofast -ffast-math -funroll-loops -fopenmp greb.model.mscm.f90 greb.shell.mscm.f90 -o greb.x

export OMP_NUM_THREADS=6
export KMP_AFFINITY="verbose,none"

# move complied files to work directory
mv greb.x work/.
mv *.mod work/.

# change to work directory
cd work

# link artificial clouds forcing file for geo-engineering experiment
if [ "${cld_artificial##*.}" == "bin" ] || [ "${cld_artificial##*.}" == "ctl" ] || [ "${cld_artificial##*.}" == "" ]
then
    cld_artificial=${cld_artificial%.*}.bin
else
    cld_artificial=${cld_artificial}.bin
fi
ln -s $cld_artificial cldart

# get name for output file
artcldname=$(basename ${cld_artificial%.*})

#  generate namelist
cat >namelist <<EOF
&NUMERICS
time_flux = 3  		! length of flux corrections run [yrs]
time_ctrl = 3 		! length of control run [yrs]
time_scnr = $YEARS  	! length of scenario run [yrs]
/
&PHYSICS
 log_exp = $EXP 	! sensitivity run as set above
 dradius = $DRAD	! deviations from the earth radius around the sun in %
 log_tsurf_ext = $log_tsurf_ext
 log_hwind_ext = $log_hwind_ext
 log_omega_ext = $log_omega_ext
/
EOF

# run greb model
./greb.x
# create output directory if does not already exist
if [ ! -d ../output ]; then mkdir ../output; fi

# create filename
FILENAME=exp-${EXP}.geoeng.${artcldname}
# FILENAME = ${FILENAME}.mod

# rename scenario run output and move it to output folder
mv scenario.bin ../output/scenario.${FILENAME}.bin
mv scenario.gmean.bin ../output/scenario.gmean.${FILENAME}.bin

# calculate months of scenario run for header file
MONTHS=$(($YEARS*12))

# scenario run
cat >../output/scenario.${FILENAME}.ctl <<EOF
dset ^scenario.${FILENAME}.bin
undef 9.e27
xdef  96 linear 0 3.75
ydef  48 linear -88.125 3.75
zdef   1 linear 1 1
tdef $MONTHS linear 15jan0  1mo
vars 8
tsurf  1 0 tsurf
tatmos 1 0 tatmos
tocean 1 0 tocean
vapor  1 0 vapour
ice    1 0 ice
precip 1 0 precip
eva 1 0 eva
qcrcl 1 0 qcrcl
endvars
EOF

cat >../output/scenario.gmean.${FILENAME}.ctl <<EOF
dset ^scenario.gmean.${FILENAME}.bin
undef 9.e27
xdef 12 linear 0 3.75
ydef  1 linear -88.125 3.75
zdef  $YEARS linear 1 1
tdef  1 linear 15jan0  1mo
vars 8
tsurf  1 0 tsurf
tatmos 1 0 tatmos
tocean 1 0 tocean
vapor  1 0 vapour
ice    1 0 ice
precip 1 0 precip
eva 1 0 eva
qcrcl 1 0 qcrcl
endvars
EOF

# control run
if [ $output_control -eq 1 ]
then
# rename control run output and move it to output folder
    mv control.bin ../output/control.${FILENAME}.bin
    cat >../output/control.${FILENAME}.ctl <<EOF
dset ^control.${FILENAME}.bin
undef 9.e27
xdef  96 linear 0 3.75
ydef  48 linear -88.125 3.75
zdef   1 linear 1 1
tdef 12 linear 15jan0  1mo
vars 8
tsurf  1 0 tsurf
tatmos 1 0 tatmos
tocean 1 0 tocean
vapor  1 0 vapour
ice    1 0 ice
precip 1 0 precip
eva 1 0 eva
qcrcl 1 0 qcrcl
endvars
EOF
fi

# Greb model output Analysys and plots
# python ../plot_contours.py ../output/scenario.${FILENAME} ../output/control.default $cld_artificial
exit
