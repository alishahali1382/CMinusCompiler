#!/bin/bash

rm -r sandbox
mkdir sandbox
mkdir sandbox/ans
cp src/* sandbox
cp tests/parser/T$1/* sandbox/ans
cd sandbox
mv ans/input.txt input.txt

python compiler.py

echo =============================
if diff parse_tree.txt ans/parse_tree.txt; then
    echo "test$1 Parse Tree: OK"
fi
echo =============================
if diff syntax_errors.txt ans/syntax_errors.txt; then
    echo "test$1 Syntax Errors: OK"
fi
echo =============================
echo