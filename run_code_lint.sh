#!/bin/bash

set -eo pipefail

if [[ ${working_directory} ]]; then
   echo "Current Directory:"
   pwd
   echo "Working Directory is defined. Changing to the directory ${working_directory}"
   cd ${working_directory}
   echo "Changed Directory:"
   pwd
fi

echo "Input Image: ${INPUT_ lintimage}"
echo "Input Image: ${INPUT_ LINTIMAGE}"

if [[ -z ${lint_utility} ]]; then
   echo "lint_utility is a required environment variable"
   exit 1
else
  utility=$(which $lint_utility) 
fi

lint_commands=`echo "$lint_commands" | sed 's/[)(]//g'`
IFS="," read -a commands <<< $lint_commands

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
  # $utility $co
done
