#!/bin/bash
key="$1"
rm -r output/*${key}*
rm -r figures/*${key}*
rm -r artificial_clouds/*${key}*
rm -r artificial_clouds/art_clouds_figures/*${key}*
# rm -r /artificial_solar_radiation/*${key}*
exit
