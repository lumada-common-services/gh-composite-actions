#!/bin/bash

set -eo pipefail

echo "Maven Settings Value:"
echo "$MAVEN_SETTINGS"

chmod +x pom.xml

if [[ -z ${maven_utility} ]]; then
   echo "maven_utility is a required environment variable"
   exit 1
else
  utility=$(which $maven_utility) 
fi

maven_commands=`echo "$maven_commands" | sed 's/[)(]//g'`
IFS="," read -a commands <<< $maven_commands

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
