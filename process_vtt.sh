#!/bin/bash

for i in *.vtt
    do
        echo "Processing ${i}"
        vtt2txt "${i}"
        textfile="${i%.vtt}.txt"
        summaryfile="${i%.vtt}-summary.txt"
        ./recursively_summarize.py "${textfile}" "${summaryfile}"
    done


