#!/bin/bash

value=`cat VERSION`
build=$(date '+%Y/%m/%d %H:%M:%S')
echo "- Last Version: $value"
echo $value | awk -F. -v OFS=. 'NF==1{print ++$NF}; NF>1{if(length($NF+1)>length($NF))$(NF-1)++; $NF=sprintf("%0*d", length($NF), ($NF+1)%(10^length($NF))); print}' > VERSION
value=`cat VERSION`
echo "- New Version : $value"
echo "__version__ = '$value'" > sdkcpc/__init__.py
echo $build > sdkcpc/resources/software/BUILD
echo "- Build       : $build"

cp VERSION sdkcpc/resources/software

# rm -rf dist
# python3 setup.py sdist
# twine upload --repository testpypi dist/*

# git add .
# git commit -m "compile and upload pytest version $value"
# git push origin develop