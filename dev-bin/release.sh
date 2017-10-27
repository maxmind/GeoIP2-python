#!/bin/bash

set -eu -o pipefail

changelog=$(cat HISTORY.rst)

regex='
([0-9]+\.[0-9]+\.[0-9]+) \(([0-9]{4}-[0-9]{2}-[0-9]{2})\)
\+*

((.|
)*)
'

if [[ ! $changelog =~ $regex ]]; then
      echo "Could not find date line in change log!"
      exit 1
fi

version="${BASH_REMATCH[1]}"
date="${BASH_REMATCH[2]}"
notes="$(echo "${BASH_REMATCH[3]}" | sed -n -e '/^[0-9]\+\.[0-9]\+\.[0-9]\+/,$!p')"

if [[ "$date" !=  "$(date +"%Y-%m-%d")" ]]; then
    echo "$date is not today!"
    exit 1
fi

tag="v$version"

if [ -n "$(git status --porcelain)" ]; then
    echo ". is not clean." >&2
    exit 1
fi

# Make sure Sphinx and wheel are installed with the current python
pip install sphinx wheel

perl -pi -e "s/(?<=__version__ = ').+?(?=')/$version/gsm" geoip2/__init__.py

echo $"Test results:"
python setup.py test

echo $'\nDiff:'
git diff

echo $'\nRelease notes:'
echo "$notes"

read -e -p "Commit changes and push to origin? " should_push

if [ "$should_push" != "y" ]; then
    echo "Aborting"
    exit 1
fi

git commit -m "Update for $tag" -a

git push

message="$version

$notes"

hub release create -m "$message" "$tag"

git push --tags

python setup.py release
