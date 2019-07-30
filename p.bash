#!/bin/bash
# run script for geo-engineering scenario experiments with the Globally Resolved Energy Balance (GREB) Model
# Author: Davide Marchegiani
PROGNAME=$0

usage() {
  cat << EOF
Usage: $PROGNAME [-e <exp_num>] [-y <year_num>] [-o] ...

Possible keys:
-c <artificial_cloud_file> -> "artificial cloud to be used with exp 930"
-e <exp_num> -> "experiment number"
-o -> "save control output"
-s <SW_decrease> -> "amount of SW to be decreased in exp 931"
-y <year_num> -> "number of years of simulation"
EOF
  exit 1
}

while getopts hc:e:os:y: opt; do
  case $opt in
    (c) cld_artificial=$OPTARG;;
    (e) EXP=$OPTARG;;
    (o) output_control=1;;
    (s) sw_decr=$OPTARG;;
    (y) YEARS=$OPTARG;;
    (*) usage
  esac
done
shift "$((OPTIND - 1))"
cld_artificial=${cld_artificial:="$1"}
