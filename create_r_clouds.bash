#!/bin/bash
# run script for geo-engineering scenario experiments with the Globally Resolved Energy Balance (GREB) Model
# Author: Davide Marchegiani

# create work directory if does not already exist
if [ ! -d work ]
then
    mkdir work
else
# else clean up work directory
    rm -f work/*
fi

### compile GREB model (uncomment one of these three options)
gfortran -Ofast -ffast-math -funroll-loops -fopenmp greb.model.mscm.f90 greb.shell.mscm.f90 -o greb.x

export OMP_NUM_THREADS=6
export KMP_AFFINITY="verbose,none"

# create output directory if does not already exist
if [ ! -d ../output ]; then mkdir ../output; fi

# move complied files to work directory
mv greb.x work/.
mv *.mod work/.

# change to work directory
cd work

# experiment number for scenario run
EXP=930
# switch managing the "control" process
control=0
# length of sensitivity experiment in years
YEARS=20

#  generate namelist
cat >namelist <<EOF
&NUMERICS
time_flux = 3  		! length of flux corrections run [yrs]
time_ctrl = 3 		! length of control run [yrs]
time_scnr = $YEARS  	! length of scenario run [yrs]
/
&PHYSICS
 log_exp = $EXP     ! sensitivity run as set above
 log_control = $control     ! control run process switch
/
EOF

cld_files=../artificial_clouds/r_calibration/*.bin
nfiles=$(ls -1 $cld_files | wc -l)
count=0
for cld_file in $cld_files ; do
    rm cldart
    ((count++))
    echo ""
    echo "Iter ${count}/${nfiles}: $cld_file"
    ln -s $cld_file cldart
    # get name for output file
    name=$(basename ${cld_file%.*})

    # run greb model
    ./greb.x

    # create filename
    FILENAME=exp-${EXP}.geoeng.${name}_${YEARS}yrs

    # calculate months of scenario run for header file
    MONTHS=$(($YEARS*12))

    # SCENARIO RUN
    # rename scenario run output and move it to output folder
    mv scenario.bin ../output/r_calibration/scenario.${FILENAME}.bin
    cat >../output/r_calibration/scenario.${FILENAME}.ctl <<EOF
    dset ^scenario.${FILENAME}.bin
    undef 9.e27
    xdef  96 linear 0 3.75
    ydef  48 linear -88.125 3.75
    zdef   1 linear 1 1
    tdef $MONTHS linear 15jan0  1mo
    vars 1
    tsurf  1 0 tsurf
    endvars
EOF

    if [ -f 'scenario.gmean.bin' ]
    then
        mv scenario.gmean.bin ../output/r_calibration/scenario.gmean.${FILENAME}.bin
        cat >../output/r_calibration/scenario.gmean.${FILENAME}.ctl <<EOF
        dset ^scenario.gmean.${FILENAME}.bin
        undef 9.e27
        xdef 12 linear 0 3.75
        ydef  1 linear -88.125 3.75
        zdef  $YEARS linear 1 1
        tdef  1 linear 15jan0  1mo
        vars 1
        tsurf  1 0 tsurf
        endvars
EOF
    fi
    # control run
    if [ $control -eq 1 ]
    then
    # rename control run output and move it to output folder
        mv control.bin ../output/r_calibration/control.${FILENAME}.bin
        cat >../output/r_calibration/control.${FILENAME}.ctl <<EOF
        dset ^control.${FILENAME}.bin
        undef 9.e27
        xdef  96 linear 0 3.75
        ydef  48 linear -88.125 3.75
        zdef   1 linear 1 1
        tdef 12 linear 15jan0  1mo
        vars 1
        tsurf  1 0 tsurf
        endvars
EOF
    fi
done

exit 0
