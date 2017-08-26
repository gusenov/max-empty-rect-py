#!/bin/bash
set -x # echo on

# Usage:
#  $ ./publish.sh
#  $ ./publish.sh --repo=pypi --name=max-empty-rect-py
#  $ ./publish.sh -r=testpypi -n=max-empty-rect-py

repo="pypi"
package_name="max-empty-rect-py"

for i in "$@"
do
case $i in
    -r=*|--repo=*)
    repo="${i#*=}"
    shift # past argument=value
    ;;
    -n=*|--name=*)
    package_name="${i#*=}"
    shift # past argument=value
    ;;
esac
done

read -p "Вы уверены, что хотите провести публикацию $package_name в $repo? " -n 1 -r
echo    # (optional) move to a new line
if [[ $REPLY =~ ^[Yy]$ ]]
then
    pip uninstall "$package_name"

    python setup.py sdist upload -r $repo

    if [ "$repo" == "pypi" ]
    then
        pip install "$package_name" --user
    elif [ "$repo" == "testpypi" ]
    then
        pip install --extra-index-url https://testpypi.python.org/pypi "$package_name" --user
    fi

    pip list
    ls ~/.local/lib/python3.5/site-packages/
fi
