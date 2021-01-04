#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

echo "removing previously generated java source"
rm -rf gen
mkdir gen
echo "making temporary copy of $1.citr ..."
cp citr/$1.citr .
# generating java code
python3 citraNabhASAsaMsAdhaka.py $1.citr gen
# compile and run java code
pushd gen
javac --module-path $FX_HOME --add-modules javafx.controls,javafx.graphics $1.java
java --module-path $FX_HOME --add-modules javafx.controls,javafx.graphics $1
popd
rm -f $1.citr
