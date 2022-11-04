#!/bin/bash

set -eo pipefail

if [[ -z ${sonar_utility} ]]; then
   echo "sonar_utility is a required environment variable"
   exit 1
else
  utility=$(which $sonar_utility) 
fi

echo "Running"

sonar_commands=`echo "$sonar_commands" | sed 's/[)(]//g'`
IFS="," read -a commands <<< $sonar_commands

for i in "${commands[@]}"
do
  co="$i"
  co=`echo $co | sed 's/^[[:space:]]*//g'`
  co=`echo $co | sed 's/[[:space:]]*$//g'`
  co=`echo $co | sed "s/^\"//1"`
  co=`echo $co | sed "s/\"$//1"`
  co=`echo $co | sed 's/^[[:space:]]*//g'`
  co=`echo $co | sed 's/[[:space:]]*$//g'`
  echo "Running $utility $co"
  $utility $co
done
