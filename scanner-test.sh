#!/bin/bash

rm -r sandbox
mkdir sandbox
mkdir sandbox/ans
cp src/* sandbox
cp tests/scanner/T$1/* sandbox/ans
cd sandbox
mv ans/input.txt input.txt

python compiler.py

# catch result of diff in an if statement
if diff tokens.txt ans/tokens.txt; then
    echo "test$1 Tokens: OK"
fi
echo =============================
if diff lexical_errors.txt ans/lexical_errors.txt; then
    echo "test$1 Lexical Errors: OK"
fi
echo =============================
# diff symbol_table.txt ans/symbol_table.txt
