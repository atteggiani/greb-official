#!/bin/bash
key='ciaomamma'

while true;do
    echo -e "Are you sure you want to remove all the files containing the string '$key' in their name?\ny/n"
    read ans
    if [[ $ans == "y" ]] || [[ $ans == "yes" ]];then
        echo 'YESSAAA'
        exit
    elif [[ $ans == "n" ]] || [[ $ans == "no" ]];then
        echo 'NONEEEE'
        exit
    fi
done
