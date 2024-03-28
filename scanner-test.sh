#!/bin/bash

rm -r sandbox
mkdir sandbox
mkdir sandbox/ans
cp src/* sandbox
cp tests/scanner/T$1/* sandbox/ans
cd sandbox
mv ans/input.txt input.txt

python compiler.py

diff tokens.txt ans/tokens.txt
# echo =============================
# diff lexical_errors.txt ans/lexical_errors.txt
# echo =============================
# diff symbol_table.txt ans/symbol_table.txt
