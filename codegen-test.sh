#!/bin/bash

rm -r sandbox
mkdir sandbox
mkdir sandbox/ans
cp src/* sandbox
cp tests/codegen/$1/* sandbox/ans
cd sandbox
mv ans/input.txt input.txt

python compiler.py

if diff output.txt ans/output.txt; then
    echo "$1: OK, outputs are same."
else
    echo "$1: outputs are different. running interpreter"
    ../interpreter/tester_linux.out
fi
echo ========================
echo