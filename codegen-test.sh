#!/bin/bash

rm -r sandbox
mkdir sandbox
mkdir sandbox/ans
cp src/* sandbox
cp tests/codegen/$1/* sandbox/ans
cd sandbox
mv ans/input.txt input.txt

python compiler.py > tmp

if diff -q output.txt ans/output.txt; then
    echo "$1: OK, outputs are same."
else
    echo "$1: outputs are different. running interpreter"
    ../interpreter/tester_linux.out 2> log > result
    head -n -1 result > result.tmp
    if diff -bBq result.tmp ans/expected.txt; then
        echo "$1: OK, PRINTs are same."
    else
        echo "$1: PRINTs are different."
        echo "Expected:"
        cat ans/expected.txt
        echo "Got:"
        cat result.tmp
    fi
fi
echo ========================
echo