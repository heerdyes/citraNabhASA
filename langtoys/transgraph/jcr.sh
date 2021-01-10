#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

echo "compiling and running generator"
javac --module-path $FX_HOME --add-modules javafx.controls,javafx.graphics $1.java
java --module-path $FX_HOME --add-modules javafx.controls,javafx.graphics $1 $2.ga

echo "compiling and running generated code"
javac --module-path $FX_HOME --add-modules javafx.controls,javafx.graphics $2.java
java --module-path $FX_HOME --add-modules javafx.controls,javafx.graphics $2
