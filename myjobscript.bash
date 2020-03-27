#!/bin/bash
# run script for geo-engineering scenario experiments with the Globally Resolved Energy Balance (GREB) Model
# Author: Davide Marchegiani
PROGNAME=$0

usage() {
  cat << EOF
Usage: $PROGNAME [-e <exp_num>] [-y <year_num>] [-o] ...

Possible keys:
-a -> perform the analysis on the output with the "plot_contours.py" script
-C -> perform control run, to get the initial condition for the current experiment
-c <artificial_cloud_file> -> "artificial cloud to be used with exp 930"
-e <exp_num> -> "experiment number"
-s <artificial_sw_file> -> "artificial SW radiation to be used with exp 931"
-y <year_num> -> "experiment length (in years)"

List of experiments with suggested experiment length (in years):

--  EXP = 20 -> Abrupt 2xCO2                                        [50 years]
--  EXP = 21 -> Abrupt 4xCO2                                        [50 years]
--  EXP = 22 -> Abrupt 10xCO2                                       [50 years]
--  EXP = 23 -> Abrupt 0.5xCO2                                      [50 years]
--  EXP = 24 -> Abrupt 0xCO2d                                       [50 years]

--  EXP = 25 -> CO2-wave 30yrs-period                               [100 years]
--  EXP = 26 -> Abrupt 2xCO2 for 30yrs, then abrupt CO2-ctrl        [100 years]
--  EXP = 27 -> solar constant +27W/m2 (~2xCO2 warming)             [50 years]
--  EXP = 28 -> 11yrs solar cycle                                   [50 years]

--  EXP = 30 -> paleo solar 231 kyr BP & CO2=200ppm                 [50 years]
--  EXP = 31 -> paleo solar 231 kyr BP                              [50 years]
--  EXP = 32 -> paleo CO2=200ppm 231 kyr BP                         [50 years]

--  EXP = 35 -> solar radiation obliquity changes                   [50 years]
--  EXP = 36 -> solar radiation eccentricity changes                [50 years]
--  EXP = 37 -> solar radiation radius changes                      [50 years]

--  EXP = 40 -> partial 2xCO2 Northern hemisphere                   [50 years]
--  EXP = 41 -> partial 2xCO2 Southern hemisphere                   [50 years]
--  EXP = 42 -> partial 2xCO2 Tropics                               [50 years]
--  EXP = 43 -> partial 2xCO2 Extratropics                          [50 years]
--  EXP = 44 -> partial 2xCO2 Ocean                                 [50 years]
--  EXP = 45 -> partial 2xCO2 Land                                  [50 years]
--  EXP = 46 -> partial 2xCO2 Boreal Winter                         [50 years]
--  EXP = 47 -> partial 2xCO2 Boreal Summer                         [50 years]

--  EXP = 50 -> control-fixed tsurf and 2xCO2                       [50 years]
--  EXP = 51 -> control-fixed tsurf and 4xCO2                       [50 years]

--  EXP = 95 -> IPCC A1B scenario                                   [150 years]
--  EXP = 96 -> IPCC RCP26 scenario                                 [550 years]
--  EXP = 97 -> IPCC RCP45 scenario                                 [550 years]
--  EXP = 98 -> IPCC RCP60 scenario                                 [550 years]
--  EXP = 99 -> IPCC RCP85 scenario                                 [550 years]

--  EXP = 100 -> run model with your own CO2 forcing.
                 It should be in the format [year co2] like for the IPC
                 scenarios and variable "FILENAME" below should be the same name
                 as your CO2 forcing file, but without '.txt'

--  EXP = 230 -> run a climate change experiment with forced boundary conditions
                 (surface temperature, horizontal winds and omega) of the CMIP5
                 rcp85 ensemble mean response

--  EXP = 240 & 241 -> run an El Niño (La Niña) experiment with forced boundary
                       conditions (surface temperature, hodrizontal winds and
                       omega) of the ERA-Interim composite mean response

-- EXP = 930 -> Geo-engineering experiment with 2xCO2 and artificial cloud cover
-- EXP = 931 -> Geo-engineering experiment with 2xCO2 and artificial incoming SW
                Radiation
-- EXP = 932 -> Geo-engineering experiment with 4xCO2 and artificial incoming SW
                Radiation
EOF
  exit 1
}

while getopts haCc:e:s:y: opt; do
  case $opt in
    (e) EXP=$OPTARG;;
    (a) analyze=1;;
    (C) control=1;;
    (c) cld_artificial=$OPTARG
        EXP=930;;
    (s) sw_artificial=$OPTARG
        EXP=931;;
    (y) YEARS=$OPTARG;;
    (*) usage
  esac
done

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

# move complied files to work directory
mv greb.x work/.
mv *.mod work/.

# change to work directory
cd work

# experiment number for scenario run
((${EXP:=930}))
# 930 - Geo-Engineering experiment with the artificial clouds forcing
# 931 - Geo-Engineering experiment with the artificial SW radiation forcing

# switch managing the "control" process
((${control:=0}))

# length of sensitivity experiment in years
((${YEARS:=50}))

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
 log_control = $control     ! control run process switch
/
EOF

# run greb model
./greb.x
# create output directory if does not already exist
if [ ! -d ../output ]; then mkdir ../output; fi

# create filename
case $EXP in
    "20" ) FILENAME=exp-${EXP}.2xCO2
    ;;
    "21" ) FILENAME=exp-${EXP}.4xCO2
    ;;
    "22" ) FILENAME=exp-${EXP}.10xCO2
    ;;
    "23" ) FILENAME=exp-${EXP}.0.5xCO2
    ;;
    "24" ) FILENAME=exp-${EXP}.0xCO2
    ;;
    "25" ) FILENAME=exp-${EXP}.CO2-wave
    ;;
    "26" ) FILENAME=exp-${EXP}.CO2-step-function
    ;;
    "27" ) FILENAME=exp-${EXP}.dS0.27W
    ;;
    "28" ) FILENAME=exp-${EXP}.solar-cycle
    ;;
    "30" ) FILENAME=exp-${EXP}.solar.231K.CO2-200ppm
    ;;
    "31" ) FILENAME=exp-${EXP}.solar.231K
    ;;
    "32" ) FILENAME=exp-${EXP}.231K.CO2-200ppm
    ;;
    "35" ) FILENAME=exp-${EXP}.obliquity.${OBL}
    ;;
    "36" ) FILENAME=exp-${EXP}.eccentricity.${ECC}
    ;;
    "37" ) FILENAME=exp-${EXP}.radius.${DRAD}
    ;;
    "40" ) FILENAME=exp-${EXP}.partial.2xCO2.n-hemis
    ;;
    "41" ) FILENAME=exp-${EXP}.partial.2xCO2.s-hemis
    ;;
    "42" ) FILENAME=exp-${EXP}.partial.2xCO2.tropics
    ;;
    "43" ) FILENAME=exp-${EXP}.partial.2xCO2.extrop
    ;;
    "44" ) FILENAME=exp-${EXP}.partial.2xCO2.ocean
    ;;
    "45" ) FILENAME=exp-${EXP}.partial.2xCO2.land
    ;;
    "46" ) FILENAME=exp-${EXP}.partial.2xCO2.winter
    ;;
    "47" ) FILENAME=exp-${EXP}.partial.2xCO2.summer
    ;;
    "50" ) FILENAME=exp-${EXP}.control-fixed.tsurf.2xCO2
    ;;
    "51" ) FILENAME=exp-${EXP}.control-fixed.tsurf.4xCO2
    ;;
    "95" ) FILENAME=exp-${EXP}.IPCC.A1B
    ;;
    "96" ) FILENAME=exp-${EXP}.IPCC.RCP26
    ;;
    "97" ) FILENAME=exp-${EXP}.IPCC.RCP45
    ;;
    "98" ) FILENAME=exp-${EXP}.IPCC.RCP60
    ;;
    "99" ) FILENAME=exp-${EXP}.IPCC.RCP85
    ;;
    "100" ) FILENAME=exp-${EXP}.${CO2input}
    ;;
    "930" | "931" ) FILENAME=exp-${EXP}.geoeng.${name}
    ;;
    * ) FILENAME=exp-${EXP}
esac
FILENAME=${FILENAME}_${YEARS}yrs

# calculate months of scenario run for header file
MONTHS=$(($YEARS*12))

# SCENARIO RUN
# rename scenario run output and move it to output folder
mv scenario.bin ../output/scenario.${FILENAME}.bin
cat >../output/scenario.${FILENAME}.ctl <<EOF
dset ^scenario.${FILENAME}.bin
undef 9.e27
xdef  96 linear 0 3.75
ydef  48 linear -88.125 3.75
zdef   1 linear 1 1
tdef $MONTHS linear 15jan0  1mo
vars 9
tsurf  1 0 tsurf
tatmos 1 0 tatmos
tocean 1 0 tocean
vapor  1 0 vapour
ice    1 0 ice
precip 1 0 precip
eva 1 0 eva
qcrcl 1 0 qcrcl
sw 1 0 sw
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
vars 9
tsurf  1 0 tsurf
tatmos 1 0 tatmos
tocean 1 0 tocean
vapor  1 0 vapour
ice    1 0 ice
precip 1 0 precip
eva 1 0 eva
qcrcl 1 0 qcrcl
sw 1 0 sw
endvars
EOF
fi
# control run
if [ $control -eq 1 ]
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
vars 9
tsurf  1 0 tsurf
tatmos 1 0 tatmos
tocean 1 0 tocean
vapor  1 0 vapour
ice    1 0 ice
precip 1 0 precip
eva 1 0 eva
qcrcl 1 0 qcrcl
sw 1 0 sw
endvars
EOF
fi

cd ..
if [[ $analyze -eq 1 ]]; then
    # Greb model output Analysys and plots
    python ./plot_contours.py ./output/scenario.${FILENAME}
fi
exit 0
