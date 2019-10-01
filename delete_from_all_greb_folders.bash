#!/bin/bash
key="$1"
if ! [[ -z "$key" ]];then
    while true;do
        echo -e "Are you sure you want to remove all the files containing the string '$key' in their name?\ny/n"
        read ans
        if [[ $ans == "y" ]] || [[ $ans == "yes" ]];then
            rm -r output/*${key}*
            rm -r figures/*${key}*
            rm -r artificial_clouds/*${key}*
            rm -r artificial_clouds/art_clouds_figures/*${key}*
            # rm -r /artificial_solar_radiation/*${key}*
            echo "DONE!"
            exit
        elif [[ $ans == "n" ]] || [[ $ans == "no" ]];then
            exit
        fi
    done
fi
