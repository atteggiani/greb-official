#!/bin/bash
# run script for geo-engineering scenario experiments with the Globally Resolved Energy Balance (GREB) Model
# Author: Davide Marchegiani
PROGNAME=$0

usage() {
  cat << EOF
Usage: $PROGNAME [-e <exp_num>] [-y <year_num>] [-o] ...

Possible keys:
-a -> perform the analysis on the output with the "plot_contours.py" script
-c <artificial_cloud_file> -> "artificial cloud to be used with exp 930"
-e <exp_num> -> "experiment number"
-o -> "save control output"
-s <artificial_sw_file> -> "artificial SW radiation to be used with exp 931"
-y <year_num> -> "number of years of simulation"
EOF
  exit 1
}

while getopts hac:e:os:y: opt; do
  case $opt in
    (a) analyze=1;;
    (c) cld_artificial=$OPTARG
        EXP=930;;
    (e) EXP=$OPTARG;;
    (o) output_control=1;;
    (s) sw_artificial=$OPTARG
        EXP=931;;
    (y) YEARS=$OPTARG;;
    (*) usage
  esac
done
shift "$((OPTIND - 1))"
cld_artificial=${cld_artificial:="$1"}

# create work directory if does not already exist
if [ ! -d work ]
then
    mkdir work
else
# else clean up work directory
    rm -f work/*
fi

# experiment number for scenario run
((${EXP:=930}))
# 930 - Geo-Engineering experiment with the artificial clouds forcing
# 931 - Geo-Engineering experiment with the artificial SW radiation forcing

# flag for saving control output (1 = save control, 0 = don't save control)
((${output_control:=0}))

# length of sensitivity experiment in years
((${YEARS:=50}))

### compile GREB model (uncomment one of these three options)
gfortran -Ofast -ffast-math -funroll-loops -fopenmp greb.model.mscm.f90 greb.shell.mscm.f90 -o greb.x

export OMP_NUM_THREADS=6
export KMP_AFFINITY="verbose,none"

# move complied files to work directory
mv greb.x work/.
mv *.mod work/.

# change to work directory
cd work

# link artificial clouds forcing file for experiment 930
if [ $EXP == 930 ]; then
    # Set the name of the binary file containing the artificial clouds input for scenario
    # run (with or without .bin).
    # If no file is provided, the default one '../artificial_clouds/cld.artificial.bin' will be used.
    cld_artificial=${cld_artificial:='../artificial_clouds/cld.artificial.bin'}

    if [ "${cld_artificial##*.}" == "bin" ] || [ "${cld_artificial##*.}" == "ctl" ] || [ "${cld_artificial##*.}" == "" ]
    then
        cld_artificial=${cld_artificial%.*}.bin
    else
        cld_artificial=${cld_artificial}.bin
    fi
    ln -s $cld_artificial cldart

    # get name for output file
    name=$(basename ${cld_artificial%.*})
fi

# link artificial SW forcing file for experiment 931
if [ $EXP == 931 ]; then
    # Set the name of the binary file containing the artificial SW input for scenario
    # run (with or without .bin).
    # If no file is provided, the default one '../artificial_solar_radiation/sw.artificial.bin' will be used.
    sw_artificial=${sw_artificial:='../artificial_solar_radiation/sw.artificial.bin'}

    if [ "${sw_artificial##*.}" == "bin" ] || [ "${sw_artificial##*.}" == "ctl" ] || [ "${sw_artificial##*.}" == "" ]
    then
        sw_artificial=${sw_artificial%.*}.bin
    else
        sw_artificial=${sw_artificial}.bin
    fi
    ln -s $sw_artificial swart

    # get name for output file
    name=$(basename ${sw_artificial%.*})
fi

#  generate namelist
cat >namelist <<EOF
&NUMERICS
time_flux = 3  		! length of flux corrections run [yrs]
time_ctrl = 3 		! length of control run [yrs]
time_scnr = $YEARS  	! length of scenario run [yrs]
/
&PHYSICS
 log_exp = $EXP     ! sensitivity run as set above
/
EOF

# run greb model
./greb.x
# create output directory if does not already exist
if [ ! -d ../output ]; then mkdir ../output; fi

# create filename
FILENAME=exp-${EXP}.geoeng.${name}_${YEARS}yrs

# rename scenario run output and move it to output folder
mv scenario.bin ../output/scenario.${FILENAME}.bin

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

if [ -f 'scenario.gmean.bin' ]
then
    mv scenario.gmean.bin ../output/scenario.gmean.${FILENAME}.bin
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
fi
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

if [ $analyze -eq 1 ]; then
    # Greb model output Analysys and plots
    python ../plot_contours.py ../output/scenario.${FILENAME}
fi
exit 0
