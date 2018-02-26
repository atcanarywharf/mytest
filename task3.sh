#!/bin/bash


folder=$1

if [ -z "$folder" ]; then
  echo "No folder specified."
  read -rsn1 -p"Press any key to continue.";echo
  exit
fi


if [ ! -d "$folder" ]; then
  echo "folder $folder does not exist."
  read -rsn1 -p"Press any key to continue.";echo
  exit
fi

for file in "$folder"/*
do
    if test -f $file
    then
        echo "$file:"
        python task2.py $file
    fi
    sleep .1
done
read -rsn1 -p"Press any key to continue.";echo

